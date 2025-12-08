from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
import numpy as np
import os

class TopicModeler:
    def __init__(self, num_topics=5):
        self.num_topics = num_topics

    def fit(self, documents):
        # Simple keyword-based topic assignment for demo
        self.keywords = {
            0: ['ai', 'machine', 'learning', 'technology'],
            1: ['climate', 'environment', 'change', 'global'],
            2: ['stock', 'market', 'finance', 'economy'],
            3: ['space', 'nasa', 'exploration', 'mars'],
            4: ['education', 'school', 'learning', 'tech']
        }
        return [f"Topic {i}: {', '.join(words)}" for i, words in self.keywords.items()]

    def transform(self, documents):
        topics = []
        for doc in documents:
            doc_lower = doc.lower()
            scores = []
            for topic_id, keywords in self.keywords.items():
                score = sum(1 for kw in keywords if kw in doc_lower)
                scores.append(score)
            topic = np.argmax(scores) if max(scores) > 0 else 0
            topics.append(topic)
        return topics, None

    def save_model(self, path="models/topic_model.pkl"):
        joblib.dump(self.keywords, path)

    def load_model(self, path="models/topic_model.pkl"):
        if os.path.exists(path):
            self.keywords = joblib.load(path)

class CTRPredictor:
    def __init__(self):
        self.avg_ctr = 0.1  # Default CTR

    def fit(self, X, y):
        if len(y) > 0:
            self.avg_ctr = np.mean(y)
        else:
            # Use mock training data
            mock_X = ["AI in healthcare", "Climate change news", "Stock market update", "Space exploration", "Education tech"]
            mock_y = [0.3, 0.2, 0.4, 0.1, 0.25]  # Mock CTR values
            self.avg_ctr = np.mean(mock_y)

    def predict_proba(self, X):
        # Simple prediction: return average CTR for all
        return np.full(len(X), self.avg_ctr)

    def save_model(self, path="models/ctr_model.pkl"):
        joblib.dump(self.avg_ctr, path)

    def load_model(self, path="models/ctr_model.pkl"):
        if os.path.exists(path):
            self.avg_ctr = joblib.load(path)