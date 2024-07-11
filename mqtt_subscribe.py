import paho.mqtt.client as mqtt
import json
import database_connection as dc
import time

# ---- MQTT Einstellungen ----
connected = False
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
broker_address = "158.180.44.197"
port = 1883
user = "bobm"
password = "letmein"
client.username_pw_set(username=user, password=password)
# ----------------------------

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Connected to broker")
        global connected
        connected = True
    else:
        print("Connection failed")

def on_message(client, userdata, msg):
    try:
        if msg.topic == "iot1/teaching_factory_fast/recipe":
            received_message = json.loads(msg.payload.decode("utf-8"))
            print(f"Message received: {received_message}")

            recipe_data = (
                received_message["recipe"],
                received_message["time"],
                received_message["color_levels_grams"]["red"],
                received_message["color_levels_grams"]["blue"],
                received_message["color_levels_grams"]["green"]
            )
            print(f"Saving recipe: {recipe_data}")
            dc.save_recipe(recipe_data)
    except ValueError as e:
        print(f"Failed to parse message: {e}")

client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_address, port=port)
client.loop_start()

client.subscribe("iot1/teaching_factory_fast/recipe")

# Keep the script running
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Disconnecting...")
    client.disconnect()
    client.loop_stop()
    print("Disconnected.")