import os
from ttn import MQTTClient

app_id = os.environ.get("TTN_APP_ID", "")  # Replace with your TTN Application ID
access_key = os.environ.get("TTN_ACCESS_KEY", "")  # Replace with your TTN Access Key

def uplink_callback(msg, client):
  print("Received message: ", msg)

handler = MQTTClient(app_id, access_key)

handler.set_uplink_callback(uplink_callback)
handler.connect()

# Now the handler is set up to receive messages and will invoke uplink_callback
# whenever a message is received.

# To keep the script running
handler.loop_forever()
