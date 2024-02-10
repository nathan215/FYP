import { Grid, Paper } from "@mui/material";
import Wrapper from "../components/Wrapper";
import MapComponent from "../components/MapComponent";

const MapRoute = () => {
  return (
    <Wrapper title="Map & Route">
      <>
        <Grid container spacing={2}>
          <Grid item xs={12} md={8} lg={9}>
            <Paper>
              <MapComponent
                mapWidth="100%"
                mapHeight="85vh"
                longitude={0}
                latitude={0}
                zooming={2}
              />
            </Paper>
          </Grid>
          <Grid item xs={12} md={4} lg={3}>
            <Paper sx={{ padding: "8px", height: "85vh" }}>
              <p style={{ margin: "8px" }}>Latitude:</p>
              <p style={{ margin: "8px" }}>Longitude:</p>
              <p style={{ margin: "8px" }}>Zoom Level:</p>
            </Paper>
          </Grid>
        </Grid>
      </>
    </Wrapper>
  );
};

export default MapRoute;
