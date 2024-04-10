import asyncio
import websockets

async def receive_messages():
    try:
        async with websockets.connect("ws://localhost:9001") as websocket:
            print("Connected to WebSocket server")
            while True:
                response = await websocket.recv()
                print("Received from server:", response)
    except Exception as e:
        print("An error occurred:", e)

# Run the client to continuously listen for messages
asyncio.run(receive_messages())