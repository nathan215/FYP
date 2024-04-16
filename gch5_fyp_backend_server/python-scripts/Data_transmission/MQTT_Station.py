import paho.mqtt.client as mqtt
import json
from shared_state import station_data, device_id  # Import the shared data structure

def save_message_to_json(message):
    with open('station_data.json', 'a') as file:
        json.dump(message, file)
        file.write('\n')  # Add newline to separate messages

def on_message(client, userdata, msg):
    print("msg")
    payload = json.loads(msg.payload.decode())
    message = {
        "device_id": payload["end_device_ids"]["device_id"],
        "gateway_id": payload["uplink_message"]["rx_metadata"][0]["gateway_ids"]["gateway_id"],
        "rssi": payload["uplink_message"]["rx_metadata"][0]["rssi"],
        "received_at": payload["uplink_message"]["rx_metadata"][0]["received_at"]
    }
    if message['device_id'] not in device_id:
        device_id.append(message['device_id'])
        print("New device_id added: ", message['device_id'])
    # Append the new message directly to the shared station_data structure
    station_data.append(message)
    print(message)
    save_message_to_json(message)

def setup_station_mqtt():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_message = on_message
    client.username_pw_set("lora-fyp-testing-2023-24@ttn", "NNSXS.V5EPTIAZDKFR2LCYERNNKDWCN6M6FSNTYYNN4QI.EM7CPT7HWOWKX2ZPUP7GBLHRLKHY245DKXJSHETTJK5QQD277HLA")
    client.connect("nam1.cloud.thethings.network", 1883, 60)
    client.subscribe("v3/lora-fyp-testing-2023-24@ttn/devices/+/up")
    client.loop_start()  # Starts network loop in a separate thread

if __name__ == "__main__":
    setup_station_mqtt()
    while True:
        pass
