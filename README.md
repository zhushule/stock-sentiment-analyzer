# Stock Sentiment Analyzer

A full-stack web app that fetches real-time stock prices and analyzes social media/news sentiment to determine bullish or bearish trends.

## Features

- Fetch real-time stock prices using Yahoo Finance.
- Display historical stock price data in a chart.
- Calculate technical indicators (RSI and MACD) for a given stock symbol.
- Perform sentiment analysis on news headlines related to a stock symbol using the VADER sentiment analysis tool.
- Provide a comprehensive trade decision based on stock data, technical indicators, and sentiment analysis.

## Technologies Used

### Frontend

- React
- Axios
- Chart.js

### Backend

- Flask
- Yahoo Finance API
- NewsAPI
- VADER Sentiment Analysis

## Project Structure

### Frontend

- `src/components/App.js`: The main component that renders the `StockPrice` and `StockChart` components.
- `src/components/StockPrice.js`: A component that allows users to enter a stock symbol and fetches the trade decision data, including the latest price, sentiment, technical indicators, and trade recommendation.
- `src/components/StockChart.js`: A component that fetches and displays the historical stock price data in a chart.
- `src/index.js`: The entry point of the React application that renders the `App` component.
- `src/App.css`: Contains the CSS styles for the `App` component.
- `src/index.css`: Contains the global CSS styles for the application.
- `src/App.test.js`: Contains tests for the `App` component.
- `src/setupTests.js`: Sets up the testing environment for the application.
- `public/index.html`: The HTML template for the React application.
- `public/manifest.json`: Contains metadata for the web application.
- `public/robots.txt`: Contains rules for web crawlers.

### Backend

- `backend/app.py`: The main Flask application file that defines the API endpoints.
- `backend/services/stock_data.py`: A service that fetches real-time and historical stock price data using Yahoo Finance.
- `backend/services/indicators.py`: A service that calculates technical indicators (RSI and MACD) for a given stock symbol.
- `backend/services/sentiment_service.py`: A service that fetches news headlines related to a stock symbol and performs sentiment analysis using the VADER sentiment analysis tool.
- `backend/requirements.txt`: Lists the dependencies required for the backend.
- `backend/.env`: Contains environment variables, such as the `NEWS_API_KEY`.

## Setup and Installation

### Prerequisites

- Node.js and npm
- Python 3.x
- pip (Python package installer)
