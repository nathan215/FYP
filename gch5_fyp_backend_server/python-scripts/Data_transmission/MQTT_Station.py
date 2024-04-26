import paho.mqtt.client as mqtt
import json
from shared_state import station_data, device_id  # Import the shared data structure
from dateutil import parser
from datetime import datetime, timedelta
import os 
dir_path = os.path.dirname(os.path.realpath(__file__))
file_path = os.path.join(dir_path, '..', '..', 'station_data.json')

def save_message_to_json(message):
    with open(file_path, 'a') as file:
        json.dump(message, file)
        file.write('\n')  # Add newline to separate messages

def on_message(client, userdata, msg):
    print("msg")
    payload = json.loads(msg.payload.decode())
    time_string = payload["uplink_message"]["received_at"]
    time_m = parser.parse(time_string)
    truncated_time_string = time_string[:-4] + 'Z'  # Remove last four characters before 'Z'
    format = '%Y-%m-%dT%H:%M:%S.%fZ'
    truncated_time = datetime.strptime(truncated_time_string, format)
    time_m += timedelta(hours=8)
    outformat = '%Y-%m-%dT%H:%M:%S.%f'
    print("Time: ", time_m.strftime(outformat))
    time_out = time_m.strftime(outformat)
    message = {
        "device_id": payload["end_device_ids"]["device_id"],
        "gateway_id": payload["uplink_message"]["rx_metadata"][0]["gateway_ids"]["gateway_id"],
        "rssi": payload["uplink_message"]["rx_metadata"][0]["rssi"],
        "time": time_out
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
