import paho.mqtt.client as mqtt

def on_message(client, userdata, msg):
    print(f"Received message: {msg.payload.decode()}")

client = mqtt.Client()
client.on_message = on_message

# Connect to the MQTT broker on your PC
client.connect("localhost", 1883, 60)

# Subscribe to the topic
client.subscribe("sensor_data_topic")

# Start the MQTT loop
client.loop_start()

try:
    while True:
        pass
except KeyboardInterrupt:
    client.disconnect()
    client.loop_stop()