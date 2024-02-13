import { Grid, Paper } from "@mui/material";
import Wrapper from "../components/Wrapper";
import MapComponent from "../components/MapComponent";

const generateRandomCoordinate = () => {
  const latitude = getRandomNumberInRange(22, 25);
  const longitude = getRandomNumberInRange(113, 114);
  return { latitude, longitude };
};

const getRandomNumberInRange = (min: number, max: number) => {
  return Math.random() * (max - min) + min;
};

const MapRoute = () => {
  const randomCoordinate = generateRandomCoordinate();

  return (
    <Wrapper title="Map & Route">
      <>
        <Grid container spacing={2}>
          <Grid item xs={12} md={8} lg={9}>
            <Paper>
              <MapComponent
                mapWidth="100%"
                mapHeight="85vh"
                longitude={randomCoordinate.longitude}
                latitude={randomCoordinate.latitude}
                zooming={13}
              />
            </Paper>
          </Grid>
          <Grid item xs={12} md={4} lg={3}>
            <Paper sx={{ padding: "8px", height: "85vh" }}>
              <p style={{ margin: "8px" }}>
                Latitude: {randomCoordinate.latitude}
              </p>
              <p style={{ margin: "8px" }}>
                Longitude: {randomCoordinate.longitude}
              </p>
              {/* <p style={{ margin: "8px" }}>Zoom Level: </p> */}
            </Paper>
          </Grid>
        </Grid>
      </>
    </Wrapper>
  );
};

export default MapRoute;
