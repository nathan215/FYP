# websocket_server.py
import json
from websocket_server import WebsocketServer

public_ip = "10.89.40.97"


class WebSocketServer:
    def __init__(self, port=9001, host=public_ip):
        self.port = port
        self.host = host
        self.server = WebsocketServer(port=self.port, host=self.host)
        self.server.set_fn_new_client(self.new_client)
        self.server.set_fn_message_received(self.message_received)
        self.server.set_fn_client_left(self.client_left)

    def new_client(self, client, server):
        print(f"New client connected and was given id {client['id']}")

    def client_left(self, client, server):
        print(f"Client({client['id']}) disconnected")

    def message_received(self, client, server, message):
        print(f"Message from Client({client['id']}): {message}")
        # Here you can handle incoming messages or commands from clients if needed

    def send_message(self, data):
        """Broadcasts data to all connected clients."""
        self.server.send_message_to_all(json.dumps(data))

    def start_server(self):
        """Starts the WebSocket server."""
        print(f"Starting WebSocket server on ws://{self.host}:{self.port}")
        self.server.run_forever()
