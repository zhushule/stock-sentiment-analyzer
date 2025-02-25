import React, { useState } from "react";
import axios from "axios";

const StockPrice = ({ setSelectedStock }) => {
  const [symbol, setSymbol] = useState("");
  const [tradeDecision, setTradeDecision] = useState(null);
  const [error, setError] = useState("");

  const fetchStockData = async () => {
    setError(""); // Clear previous errors
    setTradeDecision(null);

    if (!symbol) {
      setError("Please enter a stock symbol.");
      return;
    }

    try {
      // Fetch Trade Decision API (includes RSI, MACD, Sentiment, etc.)
      const response = await axios.get(`http://127.0.0.1:5000/api/trade-decision/${symbol}`);
      console.log("Trade Decision Data:", response.data); // Add this line for debugging
      setTradeDecision(response.data);
      setSelectedStock(symbol);
    } catch (err) {
      setError("Error fetching stock or sentiment data. Check the symbol.");
    }
  };

  return (
    <div style={{ textAlign: "center", padding: "20px" }}>
      <h2>Stock Price & Sentiment Checker</h2>
      <input
        type="text"
        placeholder="Enter Stock Symbol (e.g., AAPL)"
        value={symbol}
        onChange={(e) => setSymbol(e.target.value.toUpperCase())}
      />
      <button onClick={fetchStockData}>Get Data</button>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {tradeDecision && (
        <div>
          <h3>Stock: {tradeDecision.symbol}</h3>
          <p>Latest Price: ${tradeDecision.latest_price}</p>

          {/* Sentiment Analysis */}
          <h3>Overall Sentiment: {tradeDecision.sentiment}</h3>

          {/* Technical Indicators */}
          <h4>Technical Indicators:</h4>
          <p>RSI: {tradeDecision.RSI || "N/A"}</p>
          <p>MACD Line: {tradeDecision.MACD?.["MACD Line"] || "N/A"}</p>
          <p>Signal Line: {tradeDecision.MACD?.["Signal Line"] || "N/A"}</p>

          {/* Trade Decision */}
          <h2 style={{ color: tradeDecision.trade_decision === "BUY" ? "green" :
                       tradeDecision.trade_decision === "SELL" ? "red" : "gray" }}>
            Recommendation: {tradeDecision.trade_decision}
          </h2>

          {/* News Section */}
          <h4>Latest News:</h4>
          <ul>
            {tradeDecision.headlines && tradeDecision.headlines.length > 0 ? (
              tradeDecision.headlines.map((headline, index) => (
                <li key={index}>
                  <a href={headline.url} target="_blank" rel="noopener noreferrer">
                    {headline.title}
                  </a> - {headline.sentiment}
                </li>
              ))
            ) : (
              <p>No news available.</p>
            )}
          </ul>
        </div>
      )}
    </div>
  );
};

export default StockPrice;
