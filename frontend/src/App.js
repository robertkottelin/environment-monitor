import { makeStyles } from "@material-ui/core";
// import "./App.css";
import Header from "./Header";

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
  return (
    <div className={classes.App}>
       <Header />
    </div>
  );
}

export default App;
