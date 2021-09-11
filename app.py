import json
import time

import paho.mqtt.client as mqtt

id = '0eae5b2e-4fb0-42cb-a639-f824ccaae930'

client_telemetry_topic = id + '/telemetry'
client_name = id + 'nightlight_server'
server_command_topic = id + '/commands'

mqtt_client = mqtt.Client(client_name)
mqtt_client.connect('test.mosquitto.org')

mqtt_client.loop_start()

def handle_telemetry(client, userdata, message):
    payload = json.loads(message.payload.decode())
    print("Message received:", payload)

    #if value is less than 100, command = true
    command = { 'led_on' : payload['light'] < 100 }
    print("Sending message:", command)

    #publish to the server_command topic
    client.publish(server_command_topic, json.dumps(command))

#subscribe to the client telemetry topic to receive the light value
mqtt_client.subscribe(client_telemetry_topic)
mqtt_client.on_message = handle_telemetry

while True:
    time.sleep(2)