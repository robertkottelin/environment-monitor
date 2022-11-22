
import { makeStyles } from "@material-ui/core";
import "./App.css";
import { BrowserRouter, Route } from "react-router-dom";

const useStyles = makeStyles(() => ({
  App: {
    backgroundColor: "#14161a",
    color: "white",
    minHeight: "100vh",
  },
}));

function App() {
  const classes = useStyles();

  return (
    <BrowserRouter>
      <div className={classes.App}>
      </div>
      <Alert />
    </BrowserRouter>
  );
}

export default App;