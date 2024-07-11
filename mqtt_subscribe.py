import paho.mqtt.client as mqtt
import json
import time
import database_connection as dbc

# ---- MQTT Settings ----
connected = False
client = mqtt.Client()
broker_address = "158.180.44.197"
port = 1883
user = "bobm"
password = "letmein"
client.username_pw_set(username=user, password=password)
# ----------------------------

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        client.subscribe("iot1/teaching_factory/recipe")
        client.subscribe("iot1/teaching_factory/scale/final_weight")
        client.subscribe("iot1/teaching_factory/drop_oscillation")
        client.subscribe("iot1/teaching_factory/ground_truth")
        client.subscribe("iot1/teaching_factory/dispenser_red")
        client.subscribe("iot1/teaching_factory/dispenser_blue")
        client.subscribe("iot1/teaching_factory/dispenser_green")
        client.subscribe("iot1/teaching_factory/temperature")
        print("Connected to broker")
        global connected
        connected = True
    else:
        print("Connection failed")

def on_message(client, userdata, msg):
    try:
        received_message = json.loads(msg.payload.decode("utf-8"))

        if msg.topic == "iot1/teaching_factory/recipe":
            recipe_data = (
                received_message["id"],
                received_message["recipe"],
                received_message["creation_date"],
                received_message["color_levels_grams"]["red"],
                received_message["color_levels_grams"]["blue"],
                received_message["color_levels_grams"]["green"]
            )
            dbc.save_recipe(recipe_data)
            print("Recipe data saved to database")

        elif msg.topic == "iot1/teaching_factory/scale/final_weight":
            final_weight_data = (
                received_message["bottle"],
                received_message["time"],
                received_message["final_weight"]
            )
            dbc.save_final_weight(final_weight_data)
            print("Final weight data saved to database")

        elif msg.topic == "iot1/teaching_factory/drop_oscillation":
            drop_oscillation_data = (
                received_message["bottle"],
                json.dumps(received_message["drop_oscillation"])
            )
            dbc.save_drop_oscillation(drop_oscillation_data)
            print("Drop oscillation data saved to database")

        elif msg.topic == "iot1/teaching_factory/ground_truth":
            ground_truth_data = (
                received_message["bottle"],
                received_message["is_cracked"]
            )
            dbc.save_ground_truth(ground_truth_data)
            print("Ground truth data saved to database")

        elif msg.topic == "iot1/teaching_factory/dispenser_red":
            dispenser_red_data = (
                received_message["dispenser"],
                received_message["bottle"],
                received_message["time"],
                received_message["fill_level_grams"],
                received_message["recipe"],
                received_message["vibration-index"]
            )
            dbc.save_dispenser_red(dispenser_red_data)
            print("Dispenser red data saved to database")

        elif msg.topic == "iot1/teaching_factory/dispenser_blue":
            dispenser_blue_data = (
                received_message["dispenser"],
                received_message["bottle"],
                received_message["time"],
                received_message["fill_level_grams"],
                received_message["recipe"],
                received_message["vibration-index"]
            )
            dbc.save_dispenser_blue(dispenser_blue_data)
            print("Dispenser blue data saved to database")

        elif msg.topic == "iot1/teaching_factory/dispenser_green":
            dispenser_green_data = (
                received_message["dispenser"],
                received_message["bottle"],
                received_message["time"],
                received_message["fill_level_grams"],
                received_message["recipe"],
                received_message["vibration-index"]
            )
            dbc.save_dispenser_green(dispenser_green_data)
            print("Dispenser green data saved to database")

        elif msg.topic == "iot1/teaching_factory/temperature":
            temperature_data = (
                received_message["dispenser"],
                received_message["time"],
                received_message["temperature_C"]
            )
            dbc.save_temperature(temperature_data)
            print("Temperature data saved to database")

    except ValueError as e:
        print(f"Failed to parse message: {e}")

client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_address, port=port)
client.loop_start()

# Keep the script running
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Disconnecting...")
    client.disconnect()
    client.loop_stop()
    print("Disconnected.")
