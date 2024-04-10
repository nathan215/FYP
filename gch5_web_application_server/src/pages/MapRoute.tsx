import { Box, Grid, Paper } from "@mui/material";
import Wrapper from "../components/Wrapper";

import React, { useEffect, useRef, useState } from "react";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

const MapComponent = () => {
  const mapRef = useRef<L.Map | null>(null);
  const droneMarkerRef = useRef<L.CircleMarker | null>(null);
  const polylineRef = useRef<L.Polyline | null>(null);
  const [coordinates, setCoordinates] = useState({ lat: 0, lon: 0 });
  const [height, setHeight] = useState(0);
  const [rssi, setRSSI] = useState(0);
  const [destination, setDestination] = useState({ des_lat: 0, des_lon: 0 });

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
    const webSocket = new WebSocket("ws://localhost:9001");
    webSocket.onmessage = (event) => {
      const message = JSON.parse(event.data);

      if (message.type === "real_time_data") {
        const drone_latitude = message.data["lat"];
        const drone_longitude = message.data["lon"];
        const RSSI = message.data["rssi"];
        const drone_altitude = message.data["height"];

        setCoordinates({ lat: drone_latitude, lon: drone_longitude });
        setRSSI(RSSI);
        setHeight(drone_altitude);

        console.log(
          "Receive drone's coordinates: " +
            drone_latitude +
            "," +
            drone_longitude +
            " RSSI: " +
            RSSI
        );
        // Get the map and polyline references
        const map = mapRef.current;
        const polyline = polylineRef.current;

        if (map && polyline) {
          const newLatLng = L.latLng(drone_latitude, drone_longitude);

          if (droneMarkerRef.current) {
            droneMarkerRef.current.removeFrom(map);
          }

          // Add the new drone point as a red circle marker
          const droneMarker = L.circleMarker(newLatLng, {
            radius: 2,
            color: "red",
            fillColor: "red",
            fillOpacity: 1,
          }).addTo(map);
          droneMarkerRef.current = droneMarker;

          // Pan the map to the new drone point
          map.panTo(newLatLng);
        }
      } else {
        console.log(message.data);
        const destination_latitude = message.data["lat"];
        const destination_longitude = message.data["lon"];
        setDestination({
          des_lat: destination_latitude,
          des_lon: destination_longitude,
        });
        console.log(
          "Receive coordinates: " +
            destination_latitude +
            "," +
            destination_longitude
        );

        // Get the map and polyline references
        const map = mapRef.current;
        const polyline = polylineRef.current;

        if (map && polyline) {
          const newLatLng = L.latLng(
            destination_latitude,
            destination_longitude
          );

          // Add the new point to the polyline
          polyline.addLatLng(newLatLng);

          // Pan the map to the new point
          map.panTo(newLatLng);
        }
      }
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
              <Box id="map" width="100%" height="85vh"></Box>
            </Paper>
          </Grid>
          <Grid item xs={12} md={4} lg={3}>
            <Paper sx={{ padding: "8px", height: "85vh" }}>
              <p style={{ margin: "8px" }}>
                <b>Drone's Location: </b>({coordinates.lat}, {coordinates.lon})
              </p>
              <p style={{ margin: "8px" }}>
                <b>Current altitude: </b>
                {height}
              </p>
              <p style={{ margin: "8px" }}>
                <b>Received Signal Strength Indicator (RSSI): </b>
                {rssi}
              </p>
              <p style={{ margin: "8px" }}>
                {" "}
                <b>Next Destination: </b>({destination.des_lat},
                {destination.des_lon})
              </p>
            </Paper>
          </Grid>
        </Grid>
      </>
    </Wrapper>
  );
};

export default MapComponent;
