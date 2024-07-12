import configparser
import paho.mqtt.client as mqtt
import json
import time
import database_connection as dbc

# ---- Read configuration file ------
config = configparser.ConfigParser()
config.read("configuration.ini")

broker_address = config['mqtt']['broker_address']
port = config.getint('mqtt', 'port')
user = config['login']['user']
password = config['login']['password']

topics = {
    "recipe": config['topics']['recipe'],
    "final_weight": config['topics']['final_weight'],
    "drop_oscillation": config['topics']['drop_oscillation'],
    "ground_truth": config['topics']['ground_truth'],
    "dispenser_red": config['topics']['dispenser_red'],
    "dispenser_blue": config['topics']['dispenser_blue'],
    "dispenser_green": config['topics']['dispenser_green'],
    "temperature": config['topics']['temperature']
}

print("\n")
print("Configuration file read successfully")
print(f"you are connected to {broker_address} on port {port} with user {user} and password {password}")
print(f"we try to connect you now...")
print("\n")

# ---- MQTT Settings ----------------
connected = False
client = mqtt.Client()

client.username_pw_set(username=user, password=password)

#-----------------------------------

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        for topic in topics.values():
            client.subscribe(topic)
        print("Connected to broker")
        print("\n\n")

        global connected
        connected = True
    else:
        print("Connection failed")
        print("\n\n")


def on_message(client, userdata, msg):
    try:
        received_message = json.loads(msg.payload.decode("utf-8"))

        if msg.topic == topics["recipe"]:
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

        elif msg.topic == topics["final_weight"]:
            final_weight_data = (
                received_message["bottle"],
                received_message["time"],
                received_message["final_weight"]
            )
            dbc.save_final_weight(final_weight_data)
            print("Final weight data saved to database")

        elif msg.topic == topics["drop_oscillation"]:
            drop_oscillation_data = (
                received_message["bottle"],
                json.dumps(received_message["drop_oscillation"])
            )
            dbc.save_drop_oscillation(drop_oscillation_data)
            print("Drop oscillation data saved to database")

        elif msg.topic == topics["ground_truth"]:
            ground_truth_data = (
                received_message["bottle"],
                received_message["is_cracked"]
            )
            dbc.save_ground_truth(ground_truth_data)
            print("Ground truth data saved to database")

        elif msg.topic == topics["dispenser_red"]:
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

        elif msg.topic == topics["dispenser_blue"]:
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

        elif msg.topic == topics["dispenser_green"]:
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

        elif msg.topic == topics["temperature"]:
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
