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
   
   function refreshPage() {
    window.location.reload(false);
  }
  
  return (
    <div className="App">
      <header className="App-header">
        <div className="col">
          <h1>Temperature Data</h1>
          <button
          onClick={refreshPage}>
            Refresh
          </button>
          {data.map(temp => 
            <div key={temp.id}>
              {temp.celsius} °C - {temp.created_at}
            </div>
            )}
        </div>
      </header>
    </div>
  );
}

export default App;
