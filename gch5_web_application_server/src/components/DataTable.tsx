import { useContext, useState } from "react";
import {
  Paper,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  TablePagination,
  Typography,
} from "@mui/material";
import { WebSocketContext } from "./WebSocketContext";

const DataTable = () => {
  const { realTimeData } = useContext(WebSocketContext);
  const [page, setPage] = useState(0);
  const rowsPerPage = 20;

  console.log(realTimeData);

  const handleChangePage = (event: any, newPage: any) => {
    setPage(newPage);
  };

  return (
    <Paper sx={{ p: 2, display: "flex", flexDirection: "column" }}>
      <Typography component="h2" variant="h6" color="primary" gutterBottom>
        Real Time Data
      </Typography>
      <Table size="small">
        <TableHead>
          <TableRow>
            <TableCell>Date</TableCell>
            <TableCell>Device EUI</TableCell>
            <TableCell>Uplink Message</TableCell>
            <TableCell>RSSI</TableCell>
            <TableCell>GPS Location</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {realTimeData && realTimeData.length > 0 ? (
            realTimeData
              .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
              .map((data, index) => (
                <TableRow key={index}>
                  <TableCell>{data.time}</TableCell>
                  <TableCell>{data.device_id}</TableCell>
                  <TableCell>N/A</TableCell>
                  <TableCell>{data.rssi}</TableCell>
                  <TableCell>
                    ({data.lon}, {data.lat})
                  </TableCell>
                </TableRow>
              ))
          ) : (
            <TableRow>
              <TableCell colSpan={5}>No real-time data available</TableCell>
            </TableRow>
          )}
        </TableBody>
      </Table>
      <TablePagination
        rowsPerPageOptions={[]}
        component="div"
        count={realTimeData ? realTimeData.length : 0}
        rowsPerPage={rowsPerPage}
        page={page}
        onPageChange={handleChangePage}
      />
    </Paper>
  );
};

export default DataTable;
