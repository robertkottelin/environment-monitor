// import { makeStyles } from "@material-ui/core";
import "./App.css";
// import Header from "./Header";
import React, {useState, useEffect} from 'react';

function App() {
  const [data, setData] = React.useState(null);

  React.useEffect(() => {
    fetch("/temperatures")
      .then((res) => res.json())
      .then((data) => setData(data.message));
      // console.log(data.message)
  }, []);
  
//   useEffect(() => {
//     const getAPI = () => {
//         // Local PostgreSQL Database
//         const API = 'http://127.0.0.1:5432/';
//         fetch(API)
//             .then((response) => {
//                 console.log(response);
//                 return response.json();
//             })
//             .then((data) => {
//                 console.log(data);
//                 setLoading(false);
//                 setApiData(data);
//             });
//     };
//     getAPI();
// }, []);

  return (
    <div className="App">
      <header className="App-header">
        <p>{!data ? "Loading..." : data}</p>
      </header>
    </div>
  );
}

export default App;
