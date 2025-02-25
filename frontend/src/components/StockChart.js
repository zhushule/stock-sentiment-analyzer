import React, { useState, useEffect } from "react";
import axios from "axios";
import { Line } from "react-chartjs-2";
import "chart.js/auto";

const StockChart = ({ symbol }) => {
  const [chartData, setChartData] = useState(null);

  useEffect(() => {
    const fetchStockHistory = async () => {
      try {
        const response = await axios.get(`http://127.0.0.1:5000/api/stock/history/${symbol}`);
        const stockHistory = response.data.history;

        if (!stockHistory || stockHistory.length === 0) {
          console.error("No stock history available for", symbol);
          return;
        }

        const dates = stockHistory.map(item => item.date);
        const prices = stockHistory.map(item => item.price);

        setChartData({
          labels: dates,
          datasets: [
            {
              label: `${symbol} Price Trend`,
              data: prices,
              borderColor: "blue",
              borderWidth: 2,
              fill: false
            }
          ]
        });
      } catch (error) {
        console.error("Error fetching stock history", error);
      }
    };

    fetchStockHistory();
  }, [symbol]);

  return (
    <div style={{ marginTop: "20px" }}>
      {chartData ? <Line data={chartData} /> : <p>Loading chart...</p>}
    </div>
  );
};

export default StockChart;
