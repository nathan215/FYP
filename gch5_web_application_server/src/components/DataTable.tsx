import {
  Paper,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
} from "@mui/material";
import Title from "./Title";

const DataTable = () => {
  return (
    <Paper sx={{ p: 2, display: "flex", flexDirection: "column" }}>
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
          <TableRow>
            <TableCell>Date</TableCell>
            <TableCell>DeviceEUI</TableCell>
            <TableCell>UplinkMessage</TableCell>
            <TableCell>GPSLocation</TableCell>
          </TableRow>
        </TableBody>
      </Table>
    </Paper>
  );
};

export default DataTable;
