import * as React from "react";
import Title from "./Title";
import { Link } from "react-router-dom";

export default function Deposits() {
  return (
    <React.Fragment>
      <Link to={"/camera-view"}>
        <Title>Drone's Camera</Title>
      </Link>
    </React.Fragment>
  );
}