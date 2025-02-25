import React, { useState } from "react";
import axios from "axios";

const StockPrice = ({ onStockSelect }) => {
  const [symbol, setSymbol] = useState("");
  const [data, setData] = useState(null);
  const [sentiment, setSentiment] = useState(null);
  const [error, setError] = useState("");

  const fetchStockData = async () => {
    setError("");
    setData(null);
    setSentiment(null);

    if (!symbol) {
      setError("Please enter a stock symbol.");
      return;
    }

    try {
      const stockResponse = await axios.get(`http://127.0.0.1:5000/api/stock/${symbol}`);
      const sentimentResponse = await axios.get(`http://127.0.0.1:5000/api/sentiment/${symbol}`);

      setData(stockResponse.data);
      setSentiment(sentimentResponse.data);
      onStockSelect(symbol);
    } catch (err) {
      setError("Error fetching stock or sentiment data. Check the symbol.");
    }
  };

  const getSentimentColor = (sentimentType) => {
    if (sentimentType === "Positive") return "green";
    if (sentimentType === "Negative") return "red";
    return "gray"; // Neutral
  };

  return (
    <div>
      <h2>Stock Price & Sentiment Checker</h2>
      <input
        type="text"
        placeholder="Enter Stock Symbol (e.g., AAPL)"
        value={symbol}
        onChange={(e) => setSymbol(e.target.value.toUpperCase())}
      />
      <button onClick={fetchStockData}>Get Data</button>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {data && (
        <div>
          <h3>Stock: {data.symbol}</h3>
          <p>Latest Price: ${data.latest_price}</p>
        </div>
      )}

      {sentiment && (
        <div>
          <h3>Overall Sentiment: {sentiment.sentiment}</h3>
          <h4>Latest News:</h4>
          <ul>
            {sentiment.headlines.map((headline, index) => (
              <li key={index} style={{ color: getSentimentColor(headline.sentiment) }}>
                <a href={headline.url} target="_blank" rel="noopener noreferrer">
                  {headline.title}
                </a> - {headline.sentiment}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default StockPrice;
