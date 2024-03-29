import { Grid } from "@mui/material";
import Wrapper from "../components/Wrapper";
import CustomCard from "../components/CustomCard";
import StorageIntegration from "../components/StorageIntegration";

const Dashboard = () => {
  return (
    <Wrapper title="Dashboard">
      <>
        <Grid container spacing={3}>
          <Grid item xs={12} md={6} lg={8}>
            <CustomCard
              title="Map & Route"
              linkTo="/map-route"
              cardHeight={350}
            />
          </Grid>
          <Grid item xs={12} md={6} lg={4}>
            <CustomCard
              title="Drone & Camera"
              linkTo="/camera-view"
              cardHeight={350}
            />
          </Grid>
          <Grid item xs={12}>
            <StorageIntegration />
          </Grid>
        </Grid>
      </>
    </Wrapper>
  );
};

export default Dashboard;
