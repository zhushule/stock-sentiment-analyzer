import os
import yfinance as yf
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend

@app.route('/')
def home():
    return jsonify({'message': 'Stock Market Sentiment Analyzer Backend is Running!'})

# API endpoint to fetch stock price
@app.route('/api/stock/<symbol>', methods=['GET'])
def get_stock_price(symbol):
    try:
        stock = yf.Ticker(symbol)
        stock_info = stock.history(period="1d")  # Get today's data

        if stock_info.empty:
            return jsonify({'error': 'Invalid stock symbol or no data found'}), 404

        latest_price = stock_info['Close'].iloc[-1]  # Get latest closing price
        return jsonify({
            'symbol': symbol.upper(),
            'latest_price': round(float(latest_price), 2)
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
