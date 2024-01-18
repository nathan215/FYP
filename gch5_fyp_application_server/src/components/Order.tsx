import React, { useState, useEffect } from "react";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import Title from "./Title";
import { Link } from "react-router-dom";

export default function Orders() {
  const [rows, setRows] = useState([]);

  const fetchData = async () => {
    try {
      const response = await fetch('http://localhost:3000/get-excel-data');
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const data = await response.json();
      setRows(data);
    } catch (error) {
      console.error("There was a problem with the fetch operation:", error);
    }
  };

  useEffect(() => {
    fetchData();
  }, []); 
  
  return (
    <>
      <Title>Real Time Data</Title>
      <Table size="small">
        <TableHead>
          <TableRow>
            <TableCell>Date</TableCell>
            <TableCell>Device EUI</TableCell>
            <TableCell>Uplink Message</TableCell>
            <TableCell>GPS Location</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {rows.map((row, index) => (
            <TableRow key={index}>
              <TableCell>{row.Date}</TableCell>
              <TableCell>{row.DeviceEUI}</TableCell>
              <TableCell>{row.UplinkMessage}</TableCell>
              <TableCell>{row.GPSLocation}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </>
  );
}
