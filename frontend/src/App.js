import React, { useState } from "react";
import StockPrice from "./components/StockPrice";
import StockChart from "./components/StockChart";

function App() {
  const [selectedStock, setSelectedStock] = useState("");

  return (
    <div style={{ textAlign: "center", padding: "20px" }}>
      <h1>Stock Market Sentiment Analyzer</h1>
      <StockPrice onStockSelect={setSelectedStock} />
      {selectedStock && <StockChart symbol={selectedStock} />}
    </div>
  );
}

export default App;
