import os
import requests
import logging
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# Configure logging
logging.basicConfig(level=logging.INFO)

def fetch_news(stock_symbol):
    """ Fetch latest news headlines related to the stock symbol from trusted sources """
    if not NEWS_API_KEY:
        logging.error("NEWS_API_KEY is missing! Check .env file")
        return [{"title": "Error: NEWS_API_KEY is missing! Check .env file", "url": "", "sentiment": "Neutral"}]

    url = f"https://newsapi.org/v2/everything?q={stock_symbol}&language=en&sortBy=publishedAt&pageSize=20&apiKey={NEWS_API_KEY}"
    logging.info(f"Fetching news for {stock_symbol} with URL: {url}")
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        articles = data.get("articles", [])

        # ✅ Log API response to check if NewsAPI is returning data
        logging.info(f"NewsAPI Response for {stock_symbol}: {data}")

        if not articles:
            logging.warning(f"No relevant news found for {stock_symbol}")
            return [{"title": "No relevant news found", "url": "", "sentiment": "Neutral"}]

        headlines = []
        for article in articles:
            if "title" in article and "url" in article:
                title = article["title"]
                url = article["url"]
                sentiment = analyze_headline_sentiment(title)  
                headlines.append({"title": title, "url": url, "sentiment": sentiment})

        return headlines if headlines else [{"title": "No relevant news found", "url": "", "sentiment": "Neutral"}]

    logging.error(f"Error fetching news data: {response.status_code}, {response.text}")
    return [{"title": f"Error fetching news data: {response.status_code}", "url": "", "sentiment": "Neutral"}]

def analyze_headline_sentiment(headline):
    """ Perform sentiment analysis on a single news headline """
    analyzer = SentimentIntensityAnalyzer()
    score = analyzer.polarity_scores(headline)["compound"]

    if score > 0.2:
        return "Positive"
    elif score < -0.2:
        return "Negative"
    else:
        return "Neutral"

def get_stock_sentiment(stock_symbol):
    """ Fetch news and determine overall stock sentiment """
    headlines = fetch_news(stock_symbol)

    sentiment_counts = {"Positive": 0, "Neutral": 0, "Negative": 0}
    for headline in headlines:
        sentiment_counts[headline["sentiment"]] += 1

    if sentiment_counts["Positive"] > sentiment_counts["Negative"]:
        overall_sentiment = "Bullish"
    elif sentiment_counts["Negative"] > sentiment_counts["Positive"]:
        overall_sentiment = "Bearish"
    else:
        overall_sentiment = "Neutral"

    # ✅ Log API response before returning
    logging.info(f"Sentiment API Response for {stock_symbol}: {overall_sentiment}, Headlines: {len(headlines)} articles")
    
    return {
        "symbol": stock_symbol.upper(),
        "sentiment": overall_sentiment,
        "headlines": headlines
    }

def analyze_sentiment_with_score(headlines):
    """ Perform sentiment analysis and give a buy/sell score """
    if not headlines:
        logging.warning("No headlines available for sentiment analysis.")
        return {"sentiment_score": 0, "trade_decision": "HOLD"}

    analyzer = SentimentIntensityAnalyzer()
    total_score = 0
    count = 0

    for headline in headlines:
        sentiment_score = analyzer.polarity_scores(headline["title"])["compound"]
        total_score += sentiment_score
        count += 1

    avg_score = total_score / count if count > 0 else 0

    # ✅ Log the sentiment score
    logging.info(f"Sentiment Analysis - Avg Score: {avg_score}, Headlines Count: {count}")

    # Define buy/sell decision thresholds
    if avg_score > 0.2:
        decision = "BUY"
    elif avg_score < -0.2:
        decision = "SELL"
    else:
        decision = "HOLD"

    return {"sentiment_score": round(avg_score, 3), "trade_decision": decision}

