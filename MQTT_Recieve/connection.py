import paho.mqtt.client as mqtt
import json
import threading

# Shared data structure for storing messages
messages = []

def setup_mqtt():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_message = on_message
    client.username_pw_set("lora-fyp-testing-2023-24@ttn", "NNSXS.V5EPTIAZDKFR2LCYERNNKDWCN6M6FSNTYYNN4QI.EM7CPT7HWOWKX2ZPUP7GBLHRLKHY245DKXJSHETTJK5QQD277HLA")
    client.connect("nam1.cloud.thethings.network", 1883, 60)
    client.subscribe("v3/lora-fyp-testing-2023-24@ttn/devices/+/up")
    client.loop_start()

# Callback when a PUBLISH message is received from the server
def on_message(client, userdata, msg):
    payload = json.loads(msg.payload.decode())
    message = {
        "device_id": payload["end_device_ids"]["device_id"],
        "gateway_id": payload["uplink_message"]["rx_metadata"][0]["gateway_ids"]["gateway_id"],
        "rssi": payload["uplink_message"]["rx_metadata"][0]["rssi"],
        "received_at": payload["uplink_message"]["rx_metadata"][0]["received_at"]
    }
    messages.append(message)
    print(message)
    # Emit the new message to all connected clients


if __name__ == '__main__':
    setup_mqtt()
    while True:
        pass

