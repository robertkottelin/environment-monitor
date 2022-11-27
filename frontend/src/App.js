// import { makeStyles } from "@material-ui/core";
import "./App.css";
// import Header from "./Header";
import React, {useState, useEffect} from 'react';
import {Button, Table, TableBody, TableCell, TableHead, TableRow, Typography} from '@mui/material';


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
          <Button 
          variant="contained"
          onClick={refreshPage}
          >
          Refresh
          </Button>
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
          {(console.log(data))}

        </div>
      </header>
    </div>
  );
}

export default App;
