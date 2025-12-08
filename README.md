# Personalized News Aggregator

A news aggregator that uses content-based filtering with topic modeling (keyword-based), user reading history, click-through rate prediction, and diversity-aware recommendations to provide personalized news feeds.

## Features

- **Topic Modeling**: Keyword-based topic assignment for news articles
- **User History Tracking**: Stores user interactions (views, clicks) with article data
- **CTR Prediction**: Predicts click-through rates using historical data
- **Diversity-Aware Recommendations**: Uses Maximal Marginal Relevance (MMR) to avoid filter bubbles
- **Data Collection**: Automatically collects user interaction data for model training

## Data Sources

### News Data
- **Primary**: NewsAPI (https://newsapi.org/) - Real-time news articles
- **Fallback**: Mock data for demonstration
- To use real data: Sign up for NewsAPI key and set in `data_fetcher.py`

### Training Data
- **User Interactions**: Collected from app usage (views, clicks)
- **Article Content**: Stored with each interaction for topic analysis
- **CTR Data**: Click-through rates learned from user behavior
- Data is saved to `user_data.json` for persistence

### Model Training
- **Topic Model**: Trained on article titles/descriptions using keyword matching
- **CTR Model**: Trained on user interaction history
- Models retrain automatically as more data is collected

## Installation

1. Clone or download the project
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Configuration

1. **NewsAPI Key** (Optional):
   - Get free API key from https://newsapi.org/
   - Set in `data_fetcher.py`: `NewsFetcher(api_key="your_key_here")`

2. **Data Storage**:
   - User data saved to `user_data.json`
   - Models saved to `models/` directory

## Usage

1. Run the application:
   ```
   python app.py
   ```

2. Open `http://127.0.0.1:5000/` in your browser

3. Interact with articles:
   - Click "Read Article" to view content
   - Click "Interested" to mark as clicked
   - System learns from your preferences

## Data Collection & Privacy

- All user interactions are stored locally in JSON format
- No personal data is sent to external servers
- Data is used only for improving recommendations
- You can delete `user_data.json` to reset learning

## Technologies Used

- Flask (web framework)
- Bootstrap 5 (UI framework)
- NumPy (numerical computing)
- Joblib (model serialization)