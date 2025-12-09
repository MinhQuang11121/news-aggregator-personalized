from flask import Flask, render_template, request, session
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = 'simple_secret'

# Mock news data
MOCK_NEWS = [
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

@app.route('/')
def home():
    if 'user_id' not in session:
        session['user_id'] = 'user_' + str(hash(request.remote_addr or 'default') % 1000)
    return render_template('index_simple.html', articles=MOCK_NEWS, user_id=session['user_id'])

@app.route('/view/<int:article_id>')
def view(article_id):
    article = MOCK_NEWS[article_id % len(MOCK_NEWS)]
    return render_template('article_simple.html', article=article)

@app.route('/click/<int:article_id>')
def click(article_id):
    return f'<h1>Clicked article {article_id}</h1><a href="/">Back</a>'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)