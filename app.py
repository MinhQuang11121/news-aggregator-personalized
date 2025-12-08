from flask import Flask, render_template, request, session, redirect, url_for
from data_fetcher import NewsFetcher
from models import TopicModeler, CTRPredictor
from user_history import UserHistory
from recommender import Recommender
import os
import numpy as np

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Initialize components
news_fetcher = NewsFetcher()
topic_modeler = TopicModeler()
ctr_predictor = CTRPredictor()
user_history = UserHistory()
recommender = Recommender(topic_modeler, ctr_predictor, user_history)

# Load or train models
def initialize_models():
    articles = news_fetcher.fetch_news()
    article_texts = [a['title'] + ' ' + a['description'] for a in articles]

    # Train topic model
    topic_modeler.fit(article_texts)
    topic_modeler.save_model()

    # Train CTR model with user data or mock data
    X, y = user_history.get_training_data()
    if not X:
        # Use mock data if no user data
        X = article_texts
        y = np.random.randint(0, 2, len(X))
    ctr_predictor.fit(X, y)
    ctr_predictor.save_model()

# Add some demo data for testing
def add_demo_data():
    if not user_history.history:  # Only add if no data exists
        demo_user = 'demo_user'
        articles = news_fetcher.fetch_news()
        # Simulate user interested in AI and tech topics
        for i, article in enumerate(articles):
            if 'ai' in (article['title'] + article['description']).lower() or 'tech' in (article['title'] + article['description']).lower():
                user_history.add_interaction(demo_user, i, clicked=True, article_data=article)
            else:
                user_history.add_interaction(demo_user, i, clicked=False, article_data=article)

if not os.path.exists('models/topic_model.pkl'):
    initialize_models()
    add_demo_data()  # Add demo data for immediate testing
else:
    topic_modeler.load_model()
    ctr_predictor.load_model()

@app.route('/')
def home():
    if 'user_id' not in session:
        session['user_id'] = 'user_' + str(hash(request.remote_addr) % 1000)
    user_id = session['user_id']

    articles = news_fetcher.fetch_news()
    recommendations = recommender.recommend(user_id, articles)

    return render_template('index.html', articles=recommendations, user_id=user_id)

@app.route('/click/<int:article_id>')
def click(article_id):
    user_id = session.get('user_id')
    if user_id:
        articles = news_fetcher.fetch_news()
        article = articles[article_id % len(articles)]
        user_history.add_interaction(user_id, article_id, clicked=True, article_data=article)
    return redirect(url_for('home'))

@app.route('/view/<int:article_id>')
def view(article_id):
    user_id = session.get('user_id')
    if user_id:
        articles = news_fetcher.fetch_news()
        article = articles[article_id % len(articles)]
        user_history.add_interaction(user_id, article_id, clicked=False, article_data=article)
    return render_template('article.html', article=article)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)