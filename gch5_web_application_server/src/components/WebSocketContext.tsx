import { ReactNode, createContext, useEffect, useState } from "react";
import { websocketURL } from "../configuration";
interface RealTimeData {
  device_id: string;
  time: string;
  rssi: number;
  lon: number;
  lat: number;
  height: number;
}
interface PredictedLocation {
  lon: number;
  lat: number;
}
interface WebSocketContextProps {
  realTimeData: RealTimeData[] | null;
  predictedLocation: PredictedLocation[] | null;
}

const WebSocketContext = createContext<WebSocketContextProps>({
  realTimeData: null,
  predictedLocation: null,
});
interface WebSocketProviderProps {
  children: ReactNode;
}

const WebSocketProvider = ({ children }: WebSocketProviderProps) => {
  const [realTimeData, setRealTimeData] = useState<RealTimeData[] | null>(null);
  const [predictedLocation, setPredictedLocation] = useState<
    PredictedLocation[] | null
  >(null);

  useEffect(() => {
    const socket = new WebSocket(websocketURL);
    socket.onmessage = (event) => {
      const incomingData = JSON.parse(event.data);
      console.log(incomingData);
      // Store the new message in local storage
      const storedData = localStorage.getItem("messageHistory");
      const messageHistory = storedData ? JSON.parse(storedData) : [];
      messageHistory.push(incomingData);
      localStorage.setItem("messageHistory", JSON.stringify(messageHistory));

      // Store data in state based on the data type
      if (incomingData.type === "real_time_data") {
        setRealTimeData((prevData) => {
          if (prevData) {
            return [...prevData, incomingData.data];
          } else {
            return [incomingData.data];
          }
        });
        localStorage.setItem("realTimeData", JSON.stringify(incomingData.data));
      } else if (incomingData.type === "predict_location") {
        setPredictedLocation((prevData) => {
          if (prevData) {
            return [...prevData, incomingData.data];
          } else {
            return [incomingData.data];
          }
        });
        localStorage.setItem(
          "predictedLocation",
          JSON.stringify(incomingData.data)
        );
      }
    };

    return () => {
      socket.close();
    };
  }, []);

  const contextValue: WebSocketContextProps = {
    realTimeData,
    predictedLocation,
  };

  return (
    <WebSocketContext.Provider value={contextValue}>
      {children}
    </WebSocketContext.Provider>
  );
};

export { WebSocketProvider, WebSocketContext };
