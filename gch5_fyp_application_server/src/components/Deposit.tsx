import * as React from "react";
import Typography from "@mui/material/Typography";
import Title from "./Title";
import { Link } from "react-router-dom";

export default function Deposits() {
  return (
    <React.Fragment>
      <Typography component="p" variant="h4">
        $3,024.00
      </Typography>
      <Typography color="text.secondary" sx={{ flex: 1 }}>
        on 15 March, 2019
      </Typography>
      <div>
        <Link to={"/camera-view"}>
          <Title>Drone's Camera</Title>{" "}
        </Link>
      </div>
    </React.Fragment>
  );
}
