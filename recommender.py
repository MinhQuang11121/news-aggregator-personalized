import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

class Recommender:
    def __init__(self, topic_model, ctr_predictor, user_history):
        self.topic_model = topic_model
        self.ctr_predictor = ctr_predictor
        self.user_history = user_history
        self.vectorizer = TfidfVectorizer(max_features=1000)

    def recommend(self, user_id, articles, num_recommendations=10, diversity_lambda=0.5):
        if not articles:
            return []

        # Get user preferences
        user_topics = self.user_history.get_user_topics(user_id, self.topic_model)

        # Predict CTR for each article
        article_texts = [a['title'] + ' ' + a['description'] for a in articles]
        ctr_scores = self.ctr_predictor.predict_proba(article_texts)

        # Get topics for articles
        topics, _ = self.topic_model.transform(article_texts)

        # Content-based scores
        content_scores = []
        for topic in topics:
            if topic in user_topics:
                content_scores.append(1.0)
            else:
                content_scores.append(0.5)  # Some baseline

        # Combine scores
        combined_scores = 0.7 * ctr_scores + 0.3 * np.array(content_scores)

        # Diversity-aware selection using MMR
        recommendations = self._mmr_selection(article_texts, combined_scores, diversity_lambda, num_recommendations)

        return [articles[i] for i in recommendations]

    def _mmr_selection(self, texts, scores, lambda_param, num):
        self.vectorizer.fit(texts)
        tfidf_matrix = self.vectorizer.transform(texts)
        
        selected = []
        remaining = list(range(len(texts)))

        while len(selected) < num and remaining:
            best_score = -np.inf
            best_idx = None

            for idx in remaining:
                relevance = scores[idx]
                diversity = 0
                if selected:
                    similarities = [cosine_similarity(tfidf_matrix[idx:idx+1], tfidf_matrix[s:s+1])[0][0] for s in selected]
                    diversity = 1 - max(similarities)
                mmr_score = lambda_param * relevance - (1 - lambda_param) * diversity
                if mmr_score > best_score:
                    best_score = mmr_score
                    best_idx = idx

            if best_idx is not None:
                selected.append(best_idx)
                remaining.remove(best_idx)

        return selected