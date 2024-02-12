import {
  Paper,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
} from "@mui/material";
import Title from "./Title";

interface Props {
  data: any[];
}

const DataTable = ({ data }: Props) => {
  return (
    <Paper sx={{ p: 2, display: "flex", flexDirection: "column" }}>
      <Title>Real Time Data</Title>
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
          {data.map((item, index) => (
            <TableRow key={index}>
              <TableCell>{item.result.received_at}</TableCell>
              <TableCell>{item.result.end_device_ids.device_id}</TableCell>
              <TableCell>
                {item.result.uplink_message?.frm_payload || "N/A"}
              </TableCell>
              <TableCell>
                {item.result.uplink_message.rx_metadata[0]?.rssi || "N/A"}
              </TableCell>
              <TableCell>
                {"N/A"},{"N/A"}
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </Paper>
  );
};

export default DataTable;
