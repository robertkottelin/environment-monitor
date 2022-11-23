import { makeStyles } from "@material-ui/core";
import "./App.css";
import Header from "./Header";
import React, {useState, useEffect} from 'react';

const useStyles = makeStyles(() => ({
  App: {
    backgroundColor: "black",
    color: "white",
    alignItems: "center",
    alignText: "center",
    justifyContent: "center",
  },
}));

function App() {
  const classes = useStyles();
  const [temperatures, setTemperatures] = useState(false);

  useEffect(() => {
    getTemperatures();
  }, []);

  function getTemperatures() {
    fetch('http://localhost:3001')
      .then(response => {
        return response.text();
      })
      .then(data => {
        setTemperatures(data);
      });
  }

  return (
    <div className={classes.App}>
      {temperatures ? temperatures : 'There is no temperature data available'}
    </div>
  );
}


export default App;
