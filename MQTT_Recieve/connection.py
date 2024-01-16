import paho.mqtt.client as mqtt
import json

# TTN MQTT server credentials
MQTT_SERVER = "nam1.cloud.thethings.network"  # Removed port from here
MQTT_PORT = 1883  # or 8883 for TLS
MQTT_USERNAME = "lora-fyp-testing-2023-24@ttn"  # Replace with your TTN Application ID
MQTT_PASSWORD = "NNSXS.G76CW7MEHL57Z63EGZ37B3F5NC5XBVZAAIIJR2I.ZMWJLERLEGLILKMGNDNKSPC32OWKOBXIV2N6CGCZWHX652YSAZKQ"
# Topic to subscribe to (replace with your actual data)
MQTT_TOPIC = "v3/lora-fyp-testing-2023-24@ttn/devices/+/up"

# Callback when the client receives a CONNACK response from the server
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    # Subscribe to the topic for device uplinks
    client.subscribe(MQTT_TOPIC)

# Callback when a PUBLISH message is received from the server
def on_message(client, userdata, msg):
    print(f"Message received on topic {msg.topic}:")
    payload = json.loads(msg.payload.decode())
    print(json.dumps(payload, indent=4))

# Create an MQTT client instance
client = mqtt.Client()

# Set the username and password for the MQTT client
client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)

# Assign the callback functions
client.on_connect = on_connect
client.on_message = on_message

# Set TLS if using port 8883 (for TLS connections only)
if MQTT_PORT == 8883:
    client.tls_set()  # Default context, no certificates

# Connect to the MQTT server
client.connect(MQTT_SERVER, MQTT_PORT, 60)

# Start the network loop
client.loop_forever()