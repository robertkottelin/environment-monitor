// import { makeStyles } from "@material-ui/core";
import "./App.css";
// import Header from "./Header";
import React, { useState, useEffect } from 'react';
import { Button, Table, TableBody, TableCell, TableHead, TableRow, Typography, Paper } from '@mui/material';
// import MyChart from './components/MyChart';
import LineChart from "./components/LineChart";
import { Data } from "./utils/Data";
import {CategoryScale} from 'chart.js'; 
import Chart from 'chart.js/auto';
Chart.register(CategoryScale);


function App() {
  const [data, setData] = React.useState([]);

  useEffect(() => {
    fetch(`/temperatures`)
     .then((response) => response.json())
     .then((actualData) => setData(actualData))
     .catch((err) => {
      console.log(err.message);
     });
   }, []);

  const [chartData, setChartData] = useState({
    labels: data.map((temp) => temp.created_at), 
    datasets: [
      {
        label: "Celsius ",
        data: data.map((temp) => temp.celsius),
        backgroundColor: [
          "rgba(75,192,192,1)",
          "#ecf0f1",
          "#50AF95",
          "#f3ba2f",
          "#2a71d0"
        ],
        borderColor: "black",
        borderWidth: 2
      }
    ]
  });


   function refreshPage() {
    window.location.reload(false);
  }

  return (
    <div className="App">
      <header className="App-header">
        <div className="col">
          <Typography variant="h3">
          Temperature Data
          </Typography>
          <LineChart chartData={chartData} />
          {console.log(chartData)}
          <Button variant="contained" onClick={refreshPage}>Refresh</Button>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Celsius (°C)</TableCell>
                <TableCell>Date (UTC)</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {data.map(temp => (
                <TableRow key={temp.id}>
                  <TableCell>{temp.celsius}</TableCell>
                  <TableCell>{temp.created_at}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      </header>
      {(console.log(data))}
    </div>
  );
}

export default App;
