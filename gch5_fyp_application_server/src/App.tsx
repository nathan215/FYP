import { Link, Route, Routes } from "react-router-dom";
import "./App.css";
import Home from "./pages/Home";
import CameraView from "./pages/CameraView";
import MapRoute from "./pages/MapRoute";
import RealTimeData from "./pages/RealTimeData";

function App() {
  return (
    <>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/camera-view" element={<CameraView />} />
        <Route path="/map-route" element={<MapRoute />} />
        <Route path="/real-time-data" element={<RealTimeData />} />
      </Routes>
    </>
  );
}

export default App;

