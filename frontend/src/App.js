// import { makeStyles } from "@material-ui/core";
import "./App.css";
// import Header from "./Header";
import React, {useState, useEffect} from 'react';


function App() {
  const [data, setData] = React.useState(null);
  const [temperatures, setTemperatures] = React.useState(null);

  React.useEffect(() => {
    fetch("/api")
      .then((res) => res.json())
      .then((data) => setData(data.message));
  }, []);

  React.useEffect(() => {
    fetch("/temperatures")
      .then((res) => res.json())
      .then((data) => setTemperatures(data.message));
  }, []);
  
  return (
    <div className="App">
      <header className="App-header">
        <p>{!data ? "Loading..." : data}</p>
        <p>{!temperatures ? "Loading..." : temperatures}</p>
      </header>
    </div>
  );
}

export default App;
