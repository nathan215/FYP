import Container from "@mui/material/Container";
import Grid from "@mui/material/Grid";
import Paper from "@mui/material/Paper";
import MapCard from "./MapCard";
import Deposits from "./Deposit";
import Orders from "./Order";
import { useEffect, useState } from "react";

const TTNDataFetcher = () => {
  const [data, setData] = useState<any[]>([]);

  useEffect(() => {
    const fetchTTNData = async () => {
      try {
        const response = await fetch("", {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Authorization: "",
          },
        });

        if (!response.ok) {
          throw new Error(`Request failed with status: ${response.status}`);
        }
        // Split response into lines and parse each line as JSON
        const lines = (await response.text()).trim().split("\n");
        const parsedData = lines.map((line) => JSON.parse(line));
        setData(parsedData);
      } catch (error: any) {
        console.error("Error fetching data:", error.message);
      }
    };

    // Call the function to fetch TTN data
    fetchTTNData();
  }, []);

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Grid container spacing={3}>
        {/* MapCard */}
        <Grid item xs={12} md={8} lg={9}>
          <Paper
            sx={{
              p: 2,
              display: "flex",
              flexDirection: "column",
              height: 240,
            }}
          >
            <MapCard />
          </Paper>
        </Grid>
        {/* Recent Deposits */}
        <Grid item xs={12} md={4} lg={3}>
          <Paper
            sx={{
              p: 2,
              display: "flex",
              flexDirection: "column",
              height: 240,
            }}
          >
            <Deposits />
          </Paper>
        </Grid>
        {/* Recent Orders */}
        <Grid item xs={12}>
          <Paper sx={{ p: 2, display: "flex", flexDirection: "column" }}>
            <Orders />
          </Paper>
        </Grid>
      </Grid>
    </Container>
    // <div>
    //   <h1>TTN Data Fetcher Component</h1>
    //   <ul>
    //     {data.map((item, index) => (
    //       <li key={index}>
    //         <strong>Received At:</strong> {item.result.received_at}
    //         <br />
    //         <strong>Device ID:</strong> {item.result.end_device_ids.device_id}
    //         {/* Display uplink_message details */}
    //         {item.result.uplink_message && (
    //           <div>
    //             <strong>Uplink Message:</strong>
    //             <ul>
    //               <li>
    //                 <strong>F Port:</strong> {item.result.uplink_message.f_port}
    //               </li>
    //               <li>
    //                 <strong>Frame Payload:</strong>{" "}
    //                 {item.result.uplink_message.frm_payload}
    //               </li>
    //               <li>
    //                 <strong>Simulated:</strong>{" "}
    //                 {item.result.uplink_message.simulated ? "Yes" : "No"}
    //               </li>
    //               <li>
    //                 <strong>Settings:</strong>
    //                 <ul>
    //                   <li>
    //                     <strong>Data Rate:</strong>{" "}
    //                     {
    //                       item.result.uplink_message.settings?.data_rate?.lora
    //                         ?.bandwidth
    //                     }
    //                   </li>
    //                   <li>
    //                     <strong>Spreading Factor:</strong>{" "}
    //                     {
    //                       item.result.uplink_message.settings?.data_rate?.lora
    //                         ?.spreading_factor
    //                     }
    //                   </li>
    //                   {/* Add more properties based on the structure of uplink_message.settings */}
    //                 </ul>
    //               </li>
    //               <li>
    //                 <strong>Frequency:</strong>{" "}
    //                 {item.result.uplink_message.settings?.frequency}
    //               </li>
    //               {/* Add more properties based on the structure of uplink_message */}
    //             </ul>
    //           </div>
    //         )}
    //       </li>
    //     ))}
    //   </ul>
    // </div>
  );
};

export default TTNDataFetcher;
