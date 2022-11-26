// import { makeStyles } from "@material-ui/core";
import "./App.css";
// import Header from "./Header";
import React, {useState, useEffect} from 'react';


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
  
  return (
    <div className="App">
      <header className="App-header">
        <div className="col">
          <h1>Temperature Data</h1>
          {data.map(temp => 
            <div key={temp.id}>
              {temp.celsius} °C
            </div>
            )}
        </div>
      </header>
    </div>
  );
}

export default App;
