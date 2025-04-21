#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import subprocess

# MQTT Broker Configuration
MQTT_BROKER = "192.168.8.100"
MQTT_PORT = 1883
MQTT_USER = "esp"
MQTT_PASS = "2AH3Bm669E9dUqYu"
MQTT_TOPIC = "+/stream"

DEBUG = True

# Define actions based on topic suffix
#def handle_light(payload):
#    print(f"Light command received: {payload}")

#def handle_instrument(payload):
#    print(f"Fan command received: {payload}")

def handle_stream(payload):
    print(f"Alert received: {payload}")

service_map = {
    "bhutan/stream": "stream-bhutan.service",
    "india/stream": "stream-india.service",
    "indonesia/stream": "stream-indonesia.service"
}

def control_service(service_name, action):
    if action not in ["start", "stop"]:
        print(f"Ignoring invalid action: {action}")
        return

    try:
        print(f"Running: systemctl {action} {service_name}")
        subprocess.run(["sudo", "systemctl", action, service_name], check=True)
        print(f"{service_name} {action}ed successfully")
    except subprocess.CalledProcessError as e:
        print(f"Failed to {action} {service_name}: {e}")

# MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
        client.subscribe(MQTT_TOPIC)
    else:
        print(f"Failed to connect, return code {rc}")


def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode(errors='replace').strip()

    if DEBUG:
        print(f"[DEBUG] MQTT: Topic='{topic}' | Payload='{payload}'")

    service = service_map.get(topic)
    if service:
        if payload.lower() == "on":
            control_service(service, "start")
        elif payload.lower() == "off":
            control_service(service, "stop")
        else:
            if DEBUG:
                print(f"[DEBUG] Ignored payload: '{payload}' for service topic")
    else:
        if DEBUG:
            print(f"[DEBUG] Topic not mapped to a service: '{topic}'")



# Set up MQTT client
client = mqtt.Client()
client.username_pw_set(MQTT_USER, MQTT_PASS)
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
client.loop_forever()
