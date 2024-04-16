import "./App.css";
import { Route, Routes } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import MapRoute from "./pages/MapRoute";
import DroneCamera from "./pages/DroneCamera";
import RealTimeData from "./pages/RealTimeData";

function App() {
  return (
    <>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/map-route" element={<MapRoute />} />
        <Route path="/camera-view" element={<DroneCamera />} />
        <Route path="/real-time-data" element={<RealTimeData />} />
      </Routes>
    </>
  );
}

export default App;
