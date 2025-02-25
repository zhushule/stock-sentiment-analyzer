import yfinance as yf

def get_stock_data(symbol):
    """ Fetch real-time and historical stock price data """
    stock = yf.Ticker(symbol)
    history = stock.history(period="6mo")  # Get last 6 months' data

    if history.empty:
        return {"error": "No data found"}

    return {
        "symbol": symbol.upper(),
        "latest_price": round(float(history["Close"].iloc[-1]), 2),
        "history": [{"date": str(date.date()), "price": round(float(row["Close"]), 2)} for date, row in history.iterrows()]
    }
