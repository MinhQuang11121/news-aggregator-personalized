import json
from datetime import datetime
import os

class UserHistory:
    def __init__(self, data_file="user_data.json"):
        self.data_file = data_file
        self.history = {}  # user_id: list of (article_id, timestamp, clicked, article_data)
        self.load_history()

    def add_interaction(self, user_id, article_id, clicked=False, article_data=None):
        if user_id not in self.history:
            self.history[user_id] = []
        interaction = {
            'article_id': article_id,
            'timestamp': datetime.now().isoformat(),
            'clicked': clicked,
            'article_data': article_data  # Store article content for training
        }
        self.history[user_id].append(interaction)
        self.save_history()

    def get_history(self, user_id):
        return self.history.get(user_id, [])

    def get_user_topics(self, user_id, topic_model):
        history = self.get_history(user_id)
        clicked_articles = [h for h in history if h['clicked']]
        if not clicked_articles:
            return []
        # Get topics from clicked articles
        topics = []
        for h in clicked_articles:
            if h['article_data']:
                text = h['article_data']['title'] + ' ' + h['article_data']['description']
                topic, _ = topic_model.transform([text])
                topics.extend(topic)
        return list(set(topics))  # Unique topics

    def get_training_data(self):
        """Extract training data for CTR prediction"""
        X = []
        y = []
        for user, interactions in self.history.items():
            for interaction in interactions:
                if interaction['article_data']:
                    # Features: title + description
                    text = interaction['article_data']['title'] + ' ' + interaction['article_data']['description']
                    X.append(text)
                    y.append(1 if interaction['clicked'] else 0)
        return X, y

    def save_history(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.history, f, indent=2)

    def load_history(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                self.history = json.load(f)