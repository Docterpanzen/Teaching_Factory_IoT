import configparser
import paho.mqtt.client as mqtt
import json
import time
import requests
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

def on_disconnect(client, userdata, rc):
    global connected
    connected = False
    print("Disconnected from broker")
    if rc != 0:
        print("Unexpected disconnection. Will attempt to reconnect...")

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

def create_mqtt_client():
    client = mqtt.Client()
    client.username_pw_set(username=user, password=password)
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    return client

def try_reconnect():
    global client
    while not connected:
        try:
            if is_internet_available():
                try:
                    print("Trying to reconnect...")
                    client = create_mqtt_client()  # Re-create the client to ensure a fresh start
                    client.connect(broker_address, port=port)
                    client.loop_start()  # Restart the loop
                    time.sleep(2)  # Give it some time to connect
                except Exception as e:
                    print(f"Reconnect failed: {e}. Retrying in 2 seconds...")
            else:
                print("Internet is not available. Checking again in 2 seconds...")
            time.sleep(2)
        except KeyboardInterrupt:
            print("Interrupt received, stopping reconnect attempts.")
            break

def is_internet_available():
    try:
        response = requests.get('http://www.google.com', timeout=2)
        return True if response.status_code == 200 else False
    except requests.ConnectionError:
        return False

client = create_mqtt_client()
client.connect(broker_address, port=port)
client.loop_start()

# Keep the script running
try:
    while True:
        time.sleep(1)
        if not connected:
            try_reconnect()
except KeyboardInterrupt:
    print("Disconnecting...")
    client.disconnect()
    client.loop_stop()
    print("Disconnected.")
finally:
    client.loop_stop()
    client.disconnect()
    print("Disconnected in finally block.")
