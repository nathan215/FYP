from ttn import MQTTClient

app_id = "lora-fyp-testing-2023-24"  # Replace with your TTN Application ID
access_key = "NNSXS.VXHDZ5BNQ36IQTOZZ6QR2C6D5JCEONQCG7L2CKA.LUSJKHAIZAMFJ4ZXIKYZCE47FF5IZVU63QDKVT45DB7PWWMABAGQ"  # Replace with your TTN Access Key

def uplink_callback(msg, client):
  print("Received message: ", msg)

handler = MQTTClient(app_id, access_key)

handler.set_uplink_callback(uplink_callback)
handler.connect()

# Now the handler is set up to receive messages and will invoke uplink_callback
# whenever a message is received.

# To keep the script running
handler.loop_forever()
