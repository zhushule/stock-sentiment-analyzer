import React, { useState } from "react";
import axios from "axios";

const StockPrice = () => {
  const [symbol, setSymbol] = useState("");
  const [data, setData] = useState(null);
  const [error, setError] = useState("");

  const fetchStockPrice = async () => {
    setError(""); // Clear previous errors
    setData(null); // Clear previous results

    if (!symbol) {
      setError("Please enter a stock symbol.");
      return;
    }

    try {
      const response = await axios.get(`http://127.0.0.1:5000/api/stock/${symbol}`);
      setData(response.data);
    } catch (err) {
      setError("Error fetching stock data. Check the symbol.");
    }
  };

  return (
    <div style={{ textAlign: "center", padding: "20px" }}>
      <h2>Stock Price Checker</h2>
      <input
        type="text"
        placeholder="Enter Stock Symbol (e.g., AAPL)"
        value={symbol}
        onChange={(e) => setSymbol(e.target.value.toUpperCase())}
      />
      <button onClick={fetchStockPrice}>Get Price</button>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {data && (
        <div>
          <h3>Stock: {data.symbol}</h3>
          <p>Latest Price: ${data.latest_price}</p>
        </div>
      )}
    </div>
  );
};

export default StockPrice;
