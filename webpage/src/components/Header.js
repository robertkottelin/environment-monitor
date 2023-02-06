import { makeStyles, Button, Box, Grid } from "@material-ui/core";
// import "./App.css";
import { BrowserRouter, Route } from "react-router-dom";

const useStyles = makeStyles(() => ({
  Header: {
    backgroundColor: "black",
    color: "white",
    minHeight: "100vh",
    alignItems: "center",
    alignText: "center",
    justifyContent: "center",
  },
}));

function Header() {
  const classes = useStyles();

  function get_temperature() {
    alert('Sending API requests, hold tight!');
    // call api get_temperature()
    // store them in an array
  }
  
  return (
    <BrowserRouter>
      <div className={classes.Header}>
      <Box textAlign='center'>
        <Grid
          container
          alignItems="center"
          justifyContent="center"
          >
          <Grid>
            <Button 
              variant='contained'
              onClick={get_temperature}
            >
              Initialize temperature readings
            </Button>
          </Grid>   
        </Grid> 
      </Box>
      </div>
    </BrowserRouter>
  );
}

export default Header;
