import WebSocket from "ws";
import React from "react";

export const TestingClient = () => {
  const ws = new WebSocket("ws://localhost:8080", {
    perMessageDeflate: false,
  });

  return <div>TestingClient</div>;
};
