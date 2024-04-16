import { Box, Grid, Paper } from "@mui/material";
import Wrapper from "../components/Wrapper";
import { useContext, useEffect, useRef, useState } from "react";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import { WebSocketContext } from "../components/WebSocketContext";

const MapRoute = () => {
  const mapRef = useRef<L.Map | null>(null);
  const polylineRef = useRef<L.Polyline | null>(null);
  const markersRef = useRef<L.CircleMarker[]>([]);
  const websocketContext = useContext(WebSocketContext); // Access the WebSocket context
  const [coordinates, setCoordinates] = useState({ lat: 0, lon: 0 });
  const [height, setHeight] = useState(0);
  const [rssi, setRSSI] = useState(0);
  const [predictedLocation, setPredictedLocation] = useState<
    Array<{ lat: number; lon: number }>
  >([]);

  useEffect(() => {
    // Create the map with initial configuration
    const map = L.map("map").setView([0, 0], 18);

    // Add a tile layer to the map (e.g., OpenStreetMap tiles)
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution: "Map data © OpenStreetMap contributors",
    }).addTo(map);

    // Create a polyline for drawing the route
    const polyline = L.polyline([], { color: "blue" }).addTo(map);

    // Store references to the map and polyline
    mapRef.current = map;
    polylineRef.current = polyline;

    return () => {
      // Clean up when the component is unmounted
      map.remove();
    };
  }, []);

  useEffect(() => {
    // Access the necessary data from the WebSocket context
    const { realTimeData, predictedLocation } = websocketContext;

    if (realTimeData) {
      setCoordinates({
        lat: realTimeData[realTimeData.length - 1].lat,
        lon: realTimeData[realTimeData.length - 1].lon,
      });
      setHeight(realTimeData[realTimeData.length - 1].height);
      setRSSI(realTimeData[realTimeData.length - 1].rssi);

      // Get the map and polyline references
      const map = mapRef.current;
      const polyline = polylineRef.current;
      const markers = markersRef.current;

      if (map && polyline) {
        const newLatLng = L.latLng(
          realTimeData[realTimeData.length - 1].lat,
          realTimeData[realTimeData.length - 1].lon
        );

        // Clear previous polyline
        polyline.setLatLngs([]);

        // Add the new drone point as a red circle marker
        const droneMarker = L.circleMarker(newLatLng, {
          radius: 2,
          color: "red",
          fillColor: "red",
          fillOpacity: 1,
        }).addTo(map);
        markers.push(droneMarker);
        markers
          .slice(0, markers.length - 1)
          .forEach((marker: any) =>
            marker.setStyle({ color: "gray", fillColor: "gray" })
          );
        if (predictedLocation) {
          setPredictedLocation(predictedLocation);
          // Add the new point to the polyline
          // Add the predicted locations as part of the polyline
          const predictedLatLngs = predictedLocation.map((location) =>
            L.latLng(location.lat, location.lon)
          );
          polyline.setLatLngs(predictedLatLngs);
        }

        // Add the new point to the polyline
        polyline.addLatLng(newLatLng);

        // Pan the map to the new point
        map.panTo(newLatLng);
      }

      // Update the component state with the received data
    }
  }, [websocketContext]);

  return (
    <Wrapper title="Map & Route">
      <Grid container spacing={2}>
        <Grid item xs={12} md={8} lg={9}>
          <Paper>
            <Box id="map" style={{ height: "85vh" }} />
          </Paper>
        </Grid>
        <Grid item xs={12} md={4} lg={3}>
          <Paper sx={{ padding: "8px", height: "85vh" }}>
            <p style={{ margin: "8px", padding: "8px" }}>
              <b>Drone's Location: </b>({coordinates.lat}, {coordinates.lon})
            </p>
            <p style={{ margin: "8px", padding: "8px" }}>
              <b>Current altitude: </b>
              {height}
            </p>
            <p style={{ margin: "8px", padding: "8px" }}>
              <b>RSSI: </b>
              {rssi}
            </p>
            <p style={{ margin: "8px", padding: "8px" }}>
              <b>Next Destination: </b>({coordinates.lat}, {coordinates.lon})
            </p>
          </Paper>
        </Grid>
      </Grid>
    </Wrapper>
  );
};

export default MapRoute;
