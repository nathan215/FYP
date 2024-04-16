// import { useEffect, useState } from "react";
// import DataTable from "./DataTable";

// const StorageIntegration = () => {
//   const [data, setData] = useState<any[]>([]);

//   useEffect(() => {
//     const fetchTTNData = async () => {
//       try {
//         const response = await fetch(
//           "https://nam1.cloud.thethings.network/api/v3/as/applications/lora-fyp-testing-2023-24/packages/storage/uplink_message",
//           {
//             method: "GET",
//             headers: {
//               "Content-Type": "application/json",
//               Authorization:
//                 "Bearer NNSXS.WSDDXOK4YQ7PQOIJ7X3ZA6B2THH3AKBLS5VPX6A.E6CU6LPVPVWY7PBBPEPR4SPXU2AKP6V6EGOAQJLSGNRNEB4VNBHQ", // Replace with your actual access token
//             },
//           }
//         );

//         console.log(response);

//         if (!response.ok) {
//           throw new Error(`Request failed with status: ${response.status}`);
//         }

//         // Split response into lines and parse each line as JSON
//         const lines = (await response.text()).trim().split("\n");
//         const parsedData = lines.map((line) => JSON.parse(line));
//         setData(parsedData);
//       } catch (error: any) {
//         console.error("Error fetching data:", error.message);
//       }
//     };

//     // Call the function to fetch TTN data
//     fetchTTNData();
//   }, []);

//   return (
//     <DataTable data={data} />

//     // <div>
//     //   <h1>TTN Data Fetcher Component</h1>
//     //   <ul>
//     //     {data.map((item, index) => (
//     //       <li key={index}>
//     //         <strong>Received At:</strong> {item.result.received_at}
//     //         <br />
//     //         <strong>Device ID:</strong> {item.result.end_device_ids.device_id}
//     //         {/* Display uplink_message details */}
//     //         {item.result.uplink_message && (
//     //           <div>
//     //             <strong>Uplink Message:</strong>
//     //             <ul>
//     //               <li>
//     //                 <strong>Frame Payload:</strong>{" "}
//     //                 {item.result.uplink_message.frm_payload}
//     //               </li>
//     //               <li>
//     //                 <strong>Simulated:</strong>{" "}
//     //                 {item.result.uplink_message.simulated ? "Yes" : "No"}
//     //               </li>
//     //               <ul>
//     //                 <li>
//     //                   <strong>RSSI:</strong>{" "}
//     //                   {item.result.uplink_message.rx_metadata[0]?.rssi}
//     //                 </li>
//     //               </ul>
//     //             </ul>
//     //           </div>
//     //         )}
//     //       </li>
//     //     ))}
//     //   </ul>
//     // </div>
//   );
// };

// export default StorageIntegration;
