import { Link } from "react-router-dom";
import Header from "../components/Header/Header";

const Wrapper = () => {
  return (
    <>
      <Header />
      <nav>
        <ul>
          <li>
            <Link to={"/"}>Home Page</Link>
          </li>
          <li>
            <Link to={"/map-route"}>MapRoute</Link>
          </li>
          <li>
            <Link to={"/camera-view"}>CameraView</Link>
          </li>
          <li>
            <Link to={"/real-time-data"}>RealTimeData</Link>
          </li>
        </ul>
      </nav>
    </>
  );
};

export default Wrapper;
