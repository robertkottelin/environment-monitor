// components/LineChart.js
import React from "react";
import { Line } from "react-chartjs-2";
function LineChart({ chartData }) {
  return (
    <div className="chart-container">
      <Line
        data={chartData}
        options={{
          plugins: {
            title: {
              display: true,
              text: "Temperature Chart"
            },
            legend: {
              display: true
            }
          }
        }}
      />
    </div>
  );
}
export default LineChart;