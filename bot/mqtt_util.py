# mqtt_util.py
import os
import paho.mqtt.client as mqtt

# Load MQTT settings from environment variables
MQTT_BROKER_URL = os.getenv('MQTT_BROKER_URL')
MQTT_BROKER_PORT = int(os.getenv('MQTT_BROKER_PORT', 1883))
MQTT_TOPIC = os.getenv('MQTT_TOPIC')
MQTT_USER = os.getenv('MQTT_USERNAME')
MQTT_PASS = os.getenv('MQTT_PASSWORD')

def publish_message(topic, payload):
    def on_connect(client, userdata, flags, rc):
        print(f"Connected to MQTT Broker: {MQTT_BROKER_URL}")

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
    if MQTT_USER and MQTT_PASS:
        client.username_pw_set(MQTT_USER, MQTT_PASS)
    client.on_connect = on_connect
    client.connect(MQTT_BROKER_URL, MQTT_BROKER_PORT, 60)
    client.loop_start()
    client.publish(topic, payload)
    client.loop_stop()
    client.disconnect()