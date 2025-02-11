from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

@app.route('/')
def home():
    return jsonify({'message': 'Stock Market Sentiment Analyzer Backend is Running!'})

# Endpoint to test stock symbol input
@app.route('/api/stock/<symbol>', methods=['GET'])
def get_stock(symbol):
    return jsonify({'symbol': symbol, 'price': 123.45, 'sentiment': 'Bullish'})

if __name__ == '__main__':
    app.run(debug=True)
