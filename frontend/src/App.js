import { makeStyles } from "@material-ui/core";
import "./App.css";
import { BrowserRouter, Route } from "react-router-dom";

const useStyles = makeStyles(() => ({
  App: {
    backgroundColor: "black",
    color: "white",
    minHeight: "100vh",
  },
}));

function App() {
    const classes = useStyles();
  return (
    <BrowserRouter>
      <div className={classes.App}>
          test
      </div>
    </BrowserRouter>
  );
}

export default App;