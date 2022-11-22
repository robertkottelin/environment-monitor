import { makeStyles, Button, Box } from "@material-ui/core";
import "./App.css";
import { BrowserRouter, Route } from "react-router-dom";

const useStyles = makeStyles(() => ({
  App: {
    backgroundColor: "black",
    color: "white",
    minHeight: "100vh",
    alignItems: "center",
    alignText: "center",
  },
}));

function App() {
  const classes = useStyles();
  return (
    <BrowserRouter>
      <div className={classes.App}>
      <Box textAlign='center'>
        <Button variant='contained'>
          My button
        </Button>
      </Box>
      </div>
    </BrowserRouter>
  );
}

export default App;