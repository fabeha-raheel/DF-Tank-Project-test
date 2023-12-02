import time
import json
import paho.mqtt.publish as publish

HOSTNAME = "127.0.0.1"

def publish_sensor_data():
    # Replace with your actual sensor data retrieval logic
    sensor_data = {"temperature": 25.5, "humidity": 50.2}

    # Convert data to JSON format
    payload = json.dumps(sensor_data)

    # Publish data to the MQTT broker
    publish.single("sensor_data_topic", payload, hostname=HOSTNAME)

while True:
    publish_sensor_data()
    time.sleep(1)  # Adjust as needed