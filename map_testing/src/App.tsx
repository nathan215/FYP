import React, { useState } from "react";
import CoordinateInput from "./components/CoordinatesInput";
import MapComponent from "./components/MapComponent";

const App = () => {
  const [latitude, setLatitude] = useState(0);
  const [longitude, setLongitude] = useState(0);
  const [zooming, setZooming] = useState(2);

  const handleLatitudeChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setLatitude(parseFloat(event.target.value));
  };

  const handleLongitudeChange = (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    setLongitude(parseFloat(event.target.value));
  };

  const handleZoomingChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setZooming(parseFloat(event.target.value));
  };

  return (
    <div>
      <h1>Map & Route</h1>
      <CoordinateInput
        label="Latitude"
        value={latitude}
        onChange={handleLatitudeChange}
      />
      <CoordinateInput
        label="Longitude"
        value={longitude}
        onChange={handleLongitudeChange}
      />
      <CoordinateInput
        label="Zoom"
        value={zooming}
        onChange={handleZoomingChange}
      />
      <MapComponent
        latitude={latitude}
        longitude={longitude}
        zooming={zooming}
      />
    </div>
  );
};

export default App;
