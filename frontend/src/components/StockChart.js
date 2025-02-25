import React, { useEffect, useState } from "react";
import axios from "axios";
import { Line } from "react-chartjs-2";
import { Chart, registerables } from "chart.js";

Chart.register(...registerables);

const StockChart = ({ symbol }) => {
  const [chartData, setChartData] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!symbol) return;

    axios
      .get(`http://127.0.0.1:5000/api/stock/history/${symbol}`)
      .then((response) => {
        const history = response.data.history;

        if (!history || history.length === 0) {
          setError("No stock data available.");
          return;
        }

        const dates = history.map((entry) => entry.date);
        const prices = history.map((entry) => entry.price);

        setChartData({
          labels: dates,
          datasets: [
            {
              label: `Stock Price ($) - ${symbol}`,
              data: prices,
              fill: false,
              borderColor: "blue",
              tension: 0.1,
            },
          ],
        });
      })
      .catch(() => setError("Failed to load stock history."));
  }, [symbol]);

  return (
    <div style={{ maxWidth: "700px", margin: "auto", textAlign: "center" }}>
      <h3>Stock Price Trend</h3>
      {error ? <p style={{ color: "red" }}>{error}</p> : null}
      {chartData ? <Line data={chartData} /> : <p>Loading chart...</p>}
    </div>
  );
};

export default StockChart;
