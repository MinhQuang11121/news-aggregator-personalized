import requests
import json
from datetime import datetime, timedelta

class NewsFetcher:
    def __init__(self, api_key=None):
        self.api_key = api_key or "demo_key"  # Replace with your NewsAPI key
        self.base_url = "https://newsapi.org/v2/"

    def fetch_news(self, query="technology", days=7):
        if self.api_key != "demo_key":
            # Use real NewsAPI
            params = {
                'q': query,
                'from': (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d'),
                'sortBy': 'publishedAt',
                'apiKey': self.api_key,
                'pageSize': 20
            }
            response = requests.get(self.base_url + "everything", params=params)
            if response.status_code == 200:
                data = response.json()
                return data.get('articles', [])
            else:
                print(f"Error fetching news: {response.status_code}")
                return self._get_mock_data()
        else:
            # Use mock data for demo
            return self._get_mock_data()

    def _get_mock_data(self):
        return [
            {
                "title": "AI Advances in Healthcare",
                "description": "New AI models are revolutionizing medical diagnostics.",
                "content": "Artificial intelligence is making significant strides in healthcare...",
                "url": "https://example.com/ai-healthcare",
                "publishedAt": (datetime.now() - timedelta(days=1)).isoformat(),
                "source": {"name": "Tech News"}
            },
            {
                "title": "Climate Change Summit Results",
                "description": "World leaders agree on new climate targets.",
                "content": "The recent summit concluded with ambitious goals...",
                "url": "https://example.com/climate-summit",
                "publishedAt": (datetime.now() - timedelta(days=2)).isoformat(),
                "source": {"name": "Environment Daily"}
            },
            {
                "title": "Stock Market Trends",
                "description": "Analysis of current market conditions.",
                "content": "The stock market has shown volatility recently...",
                "url": "https://example.com/stock-market",
                "publishedAt": (datetime.now() - timedelta(days=3)).isoformat(),
                "source": {"name": "Finance Today"}
            },
            {
                "title": "Space Exploration Update",
                "description": "NASA announces new Mars mission.",
                "content": "NASA's latest mission to Mars is set to launch...",
                "url": "https://example.com/space-exploration",
                "publishedAt": (datetime.now() - timedelta(days=4)).isoformat(),
                "source": {"name": "Space News"}
            },
            {
                "title": "Education Technology Innovations",
                "description": "How edtech is transforming learning.",
                "content": "Educational technology continues to evolve...",
                "url": "https://example.com/edtech",
                "publishedAt": (datetime.now() - timedelta(days=5)).isoformat(),
                "source": {"name": "EduTech Magazine"}
            }
        ]

    def get_top_headlines(self, category="general"):
        # Mock top headlines
        return self.fetch_news()