import os
import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def fetch_news(stock_symbol):
    """ Fetch latest news headlines related to the stock symbol """
    if not NEWS_API_KEY:
        return [{"title": "Error: NEWS_API_KEY is missing! Check .env file", "url": "", "sentiment": "Neutral"}]

    url = f"https://newsapi.org/v2/everything?q={stock_symbol}&language=en&sortBy=publishedAt&pageSize=10&apiKey={NEWS_API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        articles = data.get("articles", [])

        # Extract headlines and analyze sentiment
        headlines = []
        for article in articles:
            if "title" in article:
                title = article["title"]
                url = article["url"]
                sentiment = analyze_headline_sentiment(title)  # Get sentiment score
                headlines.append({"title": title, "url": url, "sentiment": sentiment})

        return headlines if headlines else [{"title": "No relevant news found", "url": "", "sentiment": "Neutral"}]

    return [{"title": f"Error fetching news data: {response.status_code}, {response.text}", "url": "", "sentiment": "Neutral"}]

def analyze_headline_sentiment(headline):
    """ Perform sentiment analysis on a single news headline """
    analyzer = SentimentIntensityAnalyzer()
    score = analyzer.polarity_scores(headline)["compound"]

    if score > 0.05:
        return "Positive"
    elif score < -0.05:
        return "Negative"
    else:
        return "Neutral"

def get_stock_sentiment(stock_symbol):
    """ Fetch news and determine overall stock sentiment """
    headlines = fetch_news(stock_symbol)

    # Count sentiment categories
    sentiment_counts = {"Positive": 0, "Neutral": 0, "Negative": 0}
    for headline in headlines:
        sentiment_counts[headline["sentiment"]] += 1

    # Determine overall stock sentiment
    if sentiment_counts["Positive"] > sentiment_counts["Negative"]:
        overall_sentiment = "Bullish"
    elif sentiment_counts["Negative"] > sentiment_counts["Positive"]:
        overall_sentiment = "Bearish"
    else:
        overall_sentiment = "Neutral"

    return {"symbol": stock_symbol.upper(), "sentiment": overall_sentiment, "headlines": headlines}
