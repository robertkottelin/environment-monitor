import "./App.css";
import React, { useState, useEffect } from 'react';
import { Button, Table, TableBody, TableCell, TableHead, TableRow, Typography, Paper } from '@mui/material';
import { LineChart, Line, CartesianGrid, XAxis, YAxis, Tooltip } from "recharts";

function App() {
  const [data, setData] = React.useState([]);
  const [mychartdata, setMyChartData] = React.useState([]);
  const [currentchartdata, setCurrentChartData] = React.useState([]);

  useEffect(() => {
    fetch(`/temperatures`)
     .then((response) => response.json())
     .then((actualData) => setData(actualData))
     .catch((err) => {
      console.log(err.message);
     });

     fetch(`/chartdata`)
     .then((response) => response.json())
     .then((actualData) => setMyChartData(actualData))
     .catch((err) => {
      console.log(err.message);
     });

     fetch(`/currenttemperature`)
     .then((response) => response.json())
     .then((actualData) => setCurrentChartData(actualData))
     .catch((err) => {
      console.log(err.message);
     });
   }, []);

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
          <Typography variant="h6">
            Current Temperature: 
            <div>
            {currentchartdata.map((item,i) => <p key={i}>{item.celsius} °C</p>)}
            </div>
          </Typography>
          <LineChart width={800} height={200} data={mychartdata} margin={{ top: 5, right: 20, bottom: 0, left: 0 }}>
            <Line type="monotone" dataKey="celsius" stroke="#8884d8" />
            <CartesianGrid stroke="#ccc" />
            <XAxis dataKey="created_at" />
            <YAxis dataKey="celsius"/>
            <Tooltip />
          </LineChart>
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
      {/* {(console.log(data))} */}
    </div>
  );
}

export default App;
