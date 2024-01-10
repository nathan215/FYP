import * as React from "react";
import Title from "./Title";
import { Link } from "react-router-dom";

export default function MapCard() {
  return (
    <React.Fragment>
      <Link to={"/map-route"}>
        <Title>Map </Title>
      </Link>
    </React.Fragment>
  );
}
