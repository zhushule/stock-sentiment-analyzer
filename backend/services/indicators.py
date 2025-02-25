import yfinance as yf
import pandas as pd

def get_technical_indicators(symbol):
    """ Fetch RSI & MACD for stock symbol using Yahoo Finance """
    stock = yf.Ticker(symbol)
    df = stock.history(period="6mo")  # Get last 6 months of data

    if df.empty:
        return {"error": "No data found"}

    # Calculate RSI (Relative Strength Index)
    delta = df["Close"].diff()
    gain = (delta.where(delta > 0, 0)).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rs = gain / loss
    df["RSI"] = 100 - (100 / (1 + rs))

    # Calculate MACD (Moving Average Convergence Divergence)
    short_ema = df["Close"].ewm(span=12, adjust=False).mean()
    long_ema = df["Close"].ewm(span=26, adjust=False).mean()
    df["MACD"] = short_ema - long_ema
    df["Signal"] = df["MACD"].ewm(span=9, adjust=False).mean()

    return {
        "symbol": symbol.upper(),
        "RSI": round(df["RSI"].dropna().iloc[-1], 2),
        "MACD": {
            "MACD Line": round(df["MACD"].dropna().iloc[-1], 2),
            "Signal Line": round(df["Signal"].dropna().iloc[-1], 2)
        }
    }
