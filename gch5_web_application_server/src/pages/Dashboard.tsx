import { Button, Grid } from "@mui/material";
import Wrapper from "../components/Wrapper";
import CustomCard from "../components/CustomCard";
import MapCard from "../components/MapCard";
import BackendData from "../components/BackendData";
import { SpaceBar } from "@mui/icons-material";

const Dashboard = () => {
  const handleClearLocalStorage = () => {
    localStorage.clear();
    // Additional logic or actions after clearing localStorage
    // console.log("Remaining Space:", localStorage.length + " bytes");
  };
  return (
    <Wrapper title="Dashboard">
      <>
        <Grid container spacing={3}>
          <Grid item xs={12} md={6} lg={8}>
            <CustomCard
              title="Map & Route"
              linkTo="/map-route"
              cardHeight={350}
              component={<MapCard />}
            />
          </Grid>
          <Grid item xs={12} md={6} lg={4}>
            <CustomCard
              title="Drone & Camera"
              linkTo="/camera-view"
              cardHeight={350}
              component={<></>}
            />
          </Grid>
          <Grid item xs={12}>
            <BackendData />
          </Grid>
          <Grid item xs={12}>
            <Button variant="contained" onClick={handleClearLocalStorage}>
              Clear Local Storage
            </Button>
          </Grid>
        </Grid>
      </>
    </Wrapper>
  );
};

export default Dashboard;
