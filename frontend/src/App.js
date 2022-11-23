import { makeStyles } from "@material-ui/core";
// import "./App.css";
import Header from "./Header";
import React, {useState, useEffect} from 'react';


const useStyles = makeStyles(() => ({
  App: {
    backgroundColor: "black",
    color: "white",
    minHeight: "100vh",
    alignItems: "center",
    alignText: "center",
    justifyContent: "center",
  },
}));

function App() {
  const classes = useStyles();
  // const [merchants, setMerchants] = useState(false);

  // useEffect(() => {
  //   getMerchant();
  // }, []);

  // function getMerchant() {
  //   fetch('http://localhost:3001')
  //     .then(response => {
  //       return response.text();
  //     })
  //     .then(data => {
  //       setMerchants(data);
  //     });
  // }

  return (
    <div className={classes.App}>
       <Header />
    </div>
  );
}


export default App;
