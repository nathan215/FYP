import { Grid, Paper } from "@mui/material";
import Wrapper from "../components/Wrapper";
import MapComponent from "../components/MapComponent";
import { useEffect, useState } from "react";

// const generateRandomCoordinate = () => {
//   const latitude = getRandomNumberInRange(22, 25);
//   const longitude = getRandomNumberInRange(113, 114);
//   return { latitude, longitude };
// };

// const getRandomNumberInRange = (min: number, max: number) => {
//   return Math.random() * (max - min) + min;
// };

const MapRoute = () => {
  const [latitude, setLatitude] = useState<number>(0);
  const [longitude, setLongitude] = useState<number>(0);

  useEffect(() => {
    const webSocket = new WebSocket("ws://10.89.40.97:5174");

    webSocket.onopen = () => {
      console.log("WebSocket connection established");
    };

    webSocket.onmessage = (event) => {
      console.log("Receiving message: ");
      const data = JSON.parse(event.data);
      setLatitude(data.latitude);
      setLongitude(data.longitude);
    };

    webSocket.onerror = (error) => {
      console.error("WebSocket error:", error);
    };

    webSocket.onclose = () => {
      console.log("WebSocket connection closed");
    };

    return () => {
      webSocket.close();
    };
  }, []);

  return (
    <Wrapper title="Map & Route">
      <>
        <Grid container spacing={2}>
          <Grid item xs={12} md={8} lg={9}>
            <Paper>
              <MapComponent
                mapWidth="100%"
                mapHeight="85vh"
                longitude={longitude}
                latitude={latitude}
                zooming={13}
              />
            </Paper>
          </Grid>
          <Grid item xs={12} md={4} lg={3}>
            <Paper sx={{ padding: "8px", height: "85vh" }}>
              <p style={{ margin: "8px" }}>Latitude: {latitude}</p>
              <p style={{ margin: "8px" }}>Longitude: {longitude}</p>
              {/* <p style={{ margin: "8px" }}>Zoom Level: </p> */}
            </Paper>
          </Grid>
        </Grid>
      </>
    </Wrapper>
  );
};

export default MapRoute;
