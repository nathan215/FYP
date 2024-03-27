import os
import json
import pprint
import asyncio
import websockets
import paho.mqtt.client as mqtt

RC_SN = "4LFCL54005FA25"
DRONE_SN = "1581F6GKB235F00400CD"


async def send_to_websocket(message):
    uri = "ws://10.89.40.97:5174"
    async with websockets.connect(uri) as websocket:
        await websocket.send(message)
        print(f"Sent to WebSocket: {message}")


def on_subscribe(client, userdata, mid, reason_code_list, properties):
    # Since we subscribed only for a single channel, reason_code_list contains
    # a single entry
    if reason_code_list[0].is_failure:
        print(f"Broker rejected you subscription: {reason_code_list[0]}")
    else:
        print(f"Broker granted the following QoS: {reason_code_list[0].value}")


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, reason_code, properties):
    print("Connected with result code: " + str(reason_code))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("sys/#")
    client.subscribe("thing/#")


# Print interesting bits from message
def handle_osd_message(message: dict):
    data = message["data"]
    msg = {"latitude": data["latitude"], "longitude": data["longitude"]}
    asyncio.run(send_to_websocket(json.dumps(msg)))


def handle_drone_osd_message(message: dict):
    data = message["data"]
    msg = {
        "latitude": data["latitude"],
        "longitude": data["longitude"],
        "height": data["height"],
    }
    asyncio.run(send_to_websocket(json.dumps(msg)))


# The callback for when a PUBLISH message is received from the server.
def on_message(client: mqtt.Client, userdata, msg: mqtt.MQTTMessage):
    print("📨Got msg: " + msg.topic)
    message = json.loads(msg.payload.decode("utf-8"))
    if msg.topic.endswith("status"):
        if message["method"] != "update_topo":
            return
        response = {
            "tid": message["tid"],
            "bid": message["bid"],
            "timestamp": message["timestamp"] + 2,
            "data": {"result": 0},
        }
        client.publish(msg.topic + "_reply", payload=json.dumps(response))
        print("✅published")
    elif msg.topic.endswith("osd") and msg.topic.startswith("thing"):
        if RC_SN in msg.topic:
            handle_osd_message(message)
        elif DRONE_SN in msg.topic:
            handle_drone_osd_message(message)


client = mqtt.Client(
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2, transport="tcp"
)
client.on_connect = on_connect
client.on_message = on_message
client.on_subscribe = on_subscribe

client.connect("10.89.40.97", 1883, 60)
client.loop_forever()
