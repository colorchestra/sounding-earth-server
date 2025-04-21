#!/usr/bin/env python3

import paho.mqtt.client as mqtt

# MQTT Broker Configuration
MQTT_BROKER = "192.168.8.100"
MQTT_PORT = 1883
MQTT_USER = "esp"
MQTT_PASS = "your_password"
MQTT_TOPIC = "#"

# Define actions based on topic suffix
#def handle_light(payload):
#    print(f"Light command received: {payload}")

#def handle_instrument(payload):
#    print(f"Fan command received: {payload}")

def handle_stream(payload):
    print(f"Alert received: {payload}")

# Mapping topic suffixes to handler functions
topic_handlers = {
#    "light": handle_light,
#    "fan": handle_fan,
    "stream": handle_stream
}

# MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
        client.subscribe(MQTT_TOPIC)
    else:
        print(f"Failed to connect, return code {rc}")

def on_message(client, userdata, msg):
    topic_parts = msg.topic.split('/')
    command = topic_parts[-1]  # last segment
    payload = msg.payload.decode()

    print(f"Received on topic {msg.topic}: {payload}")

    handler = topic_handlers.get(command)
    if handler:
        handler(payload)
    else:
        print(f"No handler for topic suffix '{command}'")

# Set up MQTT client
client = mqtt.Client()
client.username_pw_set(MQTT_USER, MQTT_PASS)
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
client.loop_forever()
