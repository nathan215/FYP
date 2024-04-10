import { Box, Grid, Paper } from "@mui/material";
import Wrapper from "../components/Wrapper";

import React, { useEffect, useRef, useState } from "react";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

const MapComponent: React.FC = () => {
  const mapRef = useRef<L.Map | null>(null);
  const polylineRef = useRef<L.Polyline | null>(null);
  const [coordinates, setCoordinates] = useState({ lat: 0, lon: 0 });
  const webSocket = new WebSocket("ws://10.89.40.97:3000");

  useEffect(() => {
    // Create the map with initial configuration
    const map = L.map("map").setView([0, 0], 8);

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
    webSocket.onmessage = (event) => {
      const message = JSON.parse(event.data);
      console.log(message);
      if (
        message.hasOwnProperty("dronelatitude") &&
        message.hasOwnProperty("dronelongitude")
      ) {
        const { drone_latitude, drone_longitude } = message;
        console.log(message[0]);
        console.log(drone_latitude);
        setCoordinates({ lat: drone_latitude, lon: drone_longitude });
        console.log(
          "Receive drone's coordinates: " +
            drone_latitude +
            "," +
            drone_longitude
        );
        // Get the map and polyline references
        const map = mapRef.current;
        const polyline = polylineRef.current;

        if (map && polyline) {
          const newLatLng = L.latLng(drone_latitude, drone_longitude);
          // Add the new drone point as a red circle marker
          const droneMarker = L.circleMarker(newLatLng, {
            radius: 6,
            color: "red",
            fillColor: "red",
            fillOpacity: 1,
          }).addTo(map);
          // Pan the map to the new drone point
          map.panTo(newLatLng);
        }
      } else {
        const { latitude, longitude } = message;
        setCoordinates({ lat: latitude, lon: longitude });
        console.log("Receive coordinates: " + latitude + "," + longitude);

        // Get the map and polyline references
        const map = mapRef.current;
        const polyline = polylineRef.current;

        if (map && polyline) {
          const newLatLng = L.latLng(latitude, longitude);

          // Add the new point to the polyline
          polyline.addLatLng(newLatLng);

          // Pan the map to the new point
          map.panTo(newLatLng);
        }
      }
    };

    return () => {
      // webSocket.close();
      console.log(".");
    };
  }, []);
  // useEffect(() => {
  //   webSocket.onmessage = (event) => {
  //     const { latitude, longitude } = JSON.parse(event.data);
  //     setCoordinates({ lat: latitude, lon: longitude });
  //     console.log("Receive coordinates: " + latitude + "," + longitude);

  //     // Get the map and polyline references
  //     const map = mapRef.current;
  //     const polyline = polylineRef.current;

  //     if (map && polyline) {
  //       const newLatLng = L.latLng(latitude, longitude);

  //       // Add the new point to the polyline
  //       polyline.addLatLng(newLatLng);

  //       // Pan the map to the new point
  //       map.panTo(newLatLng);
  //     }
  //   };

  //   return () => {};
  // }, []);

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
              <p style={{ margin: "8px" }}>Latitude: {coordinates.lat}</p>
              <p style={{ margin: "8px" }}>Longitude: {coordinates.lon}</p>
              {/* <p style={{ margin: "8px" }}>Zoom Level: </p> */}
            </Paper>
          </Grid>
        </Grid>
      </>
    </Wrapper>
  );
};

export default MapComponent;
