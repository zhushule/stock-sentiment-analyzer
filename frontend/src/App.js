import React, { useState } from "react";
import StockPrice from "./components/StockPrice";
import StockChart from "./components/StockChart";

function App() {
  const [selectedStock, setSelectedStock] = useState(null);

  return (
    <div style={{ textAlign: "center", padding: "20px" }}>
      <h1>Stock Market Sentiment Analyzer</h1>
      <p style={{ fontStyle: "italic", color: "gray" }}>
        Get real-time stock analysis, sentiment insights, and technical indicators.
      </p>
      <hr style={{ width: "50%", margin: "20px auto" }} />

      {/* ✅ Make sure only ONE stock checker is shown */}
      <StockPrice setSelectedStock={setSelectedStock} />

      {/* ✅ Show chart only if stock is selected */}
      {selectedStock && <StockChart symbol={selectedStock} />}
    </div>
  );
}

export default App;
