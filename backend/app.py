import os
import yfinance as yf
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from services.sentiment_service import get_stock_sentiment, analyze_sentiment_with_score
from services.stock_data import get_stock_data  # ✅ FIXED: Correct Import
from services.indicators import get_technical_indicators  # ✅ FIXED: Correct Import


# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend

@app.route('/')
def home():
    return jsonify({"message": "Stock Market Sentiment Analyzer Backend is Running!"})

@app.route('/api/stock/<symbol>', methods=['GET'])
def get_stock_price(symbol):
    """ Fetch latest stock price using Yahoo Finance """
    try:
        stock = yf.Ticker(symbol)
        stock_info = stock.history(period="1d")

        if stock_info.empty:
            return jsonify({'error': 'Invalid stock symbol or no data found'}), 404

        latest_price = stock_info['Close'].iloc[-1]
        return jsonify({
            'symbol': symbol.upper(),
            'latest_price': round(float(latest_price), 2)
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stock/history/<symbol>', methods=['GET'])
def get_stock_history(symbol):
    """ Fetch last 30 days of stock price history """
    try:
        stock = yf.Ticker(symbol)
        history = stock.history(period="30d")

        if history.empty:
            return jsonify({'error': 'Invalid stock symbol or no data found'}), 404

        prices = [{"date": str(date.date()), "price": round(float(row["Close"]), 2)} for date, row in history.iterrows()]
        
        return jsonify({"symbol": symbol.upper(), "history": prices})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/sentiment/<symbol>', methods=['GET'])
def stock_sentiment(symbol):
    """ API Endpoint to get stock sentiment based on news """
    sentiment_data = get_stock_sentiment(symbol)
    return jsonify(sentiment_data)

@app.route('/api/trade-decision/<symbol>', methods=['GET'])
def trade_decision(symbol):
    """ Combine stock price, technical indicators, and sentiment to make a buy/sell decision """
    stock_data = get_stock_data(symbol)  # ✅ FIXED: This should work now
    indicators = get_technical_indicators(symbol)  # ✅ FIXED
    sentiment_data = get_stock_sentiment(symbol)  # ✅ FIXED
    
    sentiment_score = analyze_sentiment_with_score(sentiment_data["headlines"])

    return jsonify({
        "symbol": symbol.upper(),
        "latest_price": stock_data.get("latest_price", "N/A"),
        "sentiment": sentiment_data["sentiment"],
        "sentiment_score": sentiment_score["sentiment_score"],
        "trade_decision": sentiment_score["trade_decision"],
        "RSI": indicators.get("RSI", {}),
        "MACD": indicators.get("MACD", {})
    })

if __name__ == '__main__':
    app.run(debug=True)
