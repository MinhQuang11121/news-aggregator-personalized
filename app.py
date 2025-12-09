from flask import Flask, render_template, request, session
import os
from dotenv import load_dotenv
from data_fetcher import NewsFetcher
from models import TopicModeler, CTRPredictor
from recommender import Recommender
from user_history import UserHistory

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev_secret_key')

# Initialize ML components
news_fetcher = NewsFetcher()
topic_modeler = TopicModeler()
ctr_predictor = CTRPredictor()
user_history = UserHistory()
recommender = Recommender(topic_modeler, ctr_predictor, user_history)

# Load or train models
try:
    topic_modeler.load_model()
    ctr_predictor.load_model()
except:
    # Train on demo data if models don't exist
    demo_articles = [
        {"title": "AI in Healthcare", "content": "AI technology healthcare medical diagnosis"},
        {"title": "Climate Change", "content": "climate environment global warming carbon"},
        {"title": "Stock Market", "content": "finance stocks trading investment market"}
    ]
    topic_modeler.train(demo_articles)
    ctr_predictor.train(demo_articles)
    topic_modeler.save_model()
    ctr_predictor.save_model()

@app.route('/')
def home():
    if 'user_id' not in session:
        session['user_id'] = 'user_' + str(hash(request.remote_addr or 'default') % 1000)

    user_id = session['user_id']

    # Get news articles
    try:
        articles = news_fetcher.get_news()
    except:
        # Fallback to mock data if API fails
        articles = [
            {
                "title": "AI Advances in Healthcare",
                "description": "New AI models are revolutionizing medical diagnostics.",
                "content": "Artificial intelligence is making significant strides in healthcare...",
                "url": "https://example.com/ai-healthcare",
                "publishedAt": "2025-12-09T10:00:00Z",
                "source": {"name": "Tech News"}
            },
            {
                "title": "Climate Change Summit Results",
                "description": "World leaders agree on new climate targets.",
                "content": "The recent summit concluded with ambitious goals...",
                "url": "https://example.com/climate-summit",
                "publishedAt": "2025-12-08T15:30:00Z",
                "source": {"name": "Environment Daily"}
            },
            {
                "title": "Stock Market Trends",
                "description": "Analysis of current market conditions.",
                "content": "The stock market has shown volatility recently...",
                "url": "https://example.com/stock-market",
                "publishedAt": "2025-12-07T09:15:00Z",
                "source": {"name": "Finance Today"}
            }
        ]

    # Get personalized recommendations
    try:
        recommended_articles = recommender.recommend(user_id, articles, user_history)
        articles = recommended_articles[:10]  # Show top 10
    except:
        # If recommendation fails, show all articles
        pass

    return render_template('index.html', articles=articles, user_id=user_id)

@app.route('/view/<int:article_id>')
def view(article_id):
    user_id = session.get('user_id', 'anonymous')

    # Get articles (same logic as home)
    try:
        articles = news_fetcher.get_news()
    except:
        articles = [
            {
                "title": "AI Advances in Healthcare",
                "description": "New AI models are revolutionizing medical diagnostics.",
                "content": "Artificial intelligence is making significant strides in healthcare...",
                "url": "https://example.com/ai-healthcare",
                "publishedAt": "2025-12-09T10:00:00Z",
                "source": {"name": "Tech News"}
            },
            {
                "title": "Climate Change Summit Results",
                "description": "World leaders agree on new climate targets.",
                "content": "The recent summit concluded with ambitious goals...",
                "url": "https://example.com/climate-summit",
                "publishedAt": "2025-12-08T15:30:00Z",
                "source": {"name": "Environment Daily"}
            },
            {
                "title": "Stock Market Trends",
                "description": "Analysis of current market conditions.",
                "content": "The stock market has shown volatility recently...",
                "url": "https://example.com/stock-market",
                "publishedAt": "2025-12-07T09:15:00Z",
                "source": {"name": "Finance Today"}
            }
        ]

    if 0 <= article_id < len(articles):
        article = articles[article_id]

        # Track user interaction
        user_history.add_interaction(user_id, article_id, 'view')

        return render_template('article.html', article=article)
    else:
        return "Article not found", 404

@app.route('/profile')
def profile():
    user_id = session.get('user_id', 'anonymous')
    history = user_history.get_history(user_id)
    stats = {
        'total_views': len([h for h in history if not h['clicked']]),
        'total_clicks': len([h for h in history if h['clicked']]),
        'unique_articles': len(set(h['article_id'] for h in history))
    }
    return render_template('profile.html', history=history[-10:], stats=stats, user_id=user_id)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)