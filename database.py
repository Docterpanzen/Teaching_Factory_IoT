import sqlite3
import json

def create_database(db_file_path):
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS recipes (
        id INTEGER PRIMARY KEY,
        recipe TEXT,
        creation_date TEXT,
        red INTEGER,
        blue INTEGER,
        green INTEGER
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS final_weight (
        id INTEGER PRIMARY KEY,
        bottle TEXT,
        time INTEGER,
        final_weight REAL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS drop_oscillation (
        id INTEGER PRIMARY KEY,
        bottle TEXT,
        drop_oscillation TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ground_truth (
        id INTEGER PRIMARY KEY,
        bottle TEXT,
        is_cracked TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS dispenser_red (
        id INTEGER PRIMARY KEY,
        dispenser TEXT,
        bottle TEXT,
        time INTEGER,
        fill_level_grams REAL,
        recipe INTEGER,
        vibration_index REAL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS dispenser_blue (
        id INTEGER PRIMARY KEY,
        dispenser TEXT,
        bottle TEXT,
        time INTEGER,
        fill_level_grams REAL,
        recipe INTEGER,
        vibration_index REAL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS dispenser_green (
        id INTEGER PRIMARY KEY,
        dispenser TEXT,
        bottle TEXT,
        time INTEGER,
        fill_level_grams REAL,
        recipe INTEGER,
        vibration_index REAL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS temperature (
        id INTEGER PRIMARY KEY,
        dispenser TEXT,
        time INTEGER,
        temperature_C REAL
    )
    ''')

    # Commit changes and close connection
    conn.commit()
    conn.close()




def populate_database(json_file_path, db_file_path):
    # Read JSON data
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    # Connect to SQLite3 database
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()

    # Insert data into tables
    for key, value in data['iot1/teaching_factory_fast/recipe'].items():
        cursor.execute('''
        INSERT INTO recipes (id, recipe, time, red, blue, green)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (int(key), value['recipe'], value['time'], value['color_levels_grams']['red'], value['color_levels_grams']['blue'], value['color_levels_grams']['green']))

    for key, value in data['iot1/teaching_factory_fast/dispenser_red'].items():
        cursor.execute('''
        INSERT INTO dispenser_red (id, dispenser, bottle, time, fill_level_grams, recipe)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (int(key), value['dispenser'], value['bottle'], value['time'], value['fill_level_grams'], value['recipe']))

    for key, value in data['iot1/teaching_factory_fast/temperature'].items():
        cursor.execute('''
        INSERT INTO temperature (id, time, temperature_C)
        VALUES (?, ?, ?)
        ''', (int(key), value['time'], value['temperature_C']))

    for key, value in data['iot1/teaching_factory_fast/scale/final_weight'].items():
        cursor.execute('''
        INSERT INTO final_weight (id, bottle, time, final_weight)
        VALUES (?, ?, ?, ?)
        ''', (int(key), value['bottle'], value['time'], value['final_weight']))

    for key, value in data['iot1/teaching_factory_fast/dispenser_blue/vibration'].items():
        cursor.execute('''
        INSERT INTO vibration_data (id, dispenser, bottle, time, vibration_index)
        VALUES (?, ?, ?, ?, ?)
        ''', (int(key), value['dispenser'], value['bottle'], value['time'], value['vibration-index']))

    for key, value in data['iot1/teaching_factory_fast/drop_vibration'].items():
        cursor.execute('''
        INSERT INTO drop_vibration (id, bottle, drop_vibration)
        VALUES (?, ?, ?)
        ''', (int(key), value['bottle'], json.dumps(value['drop_vibration'])))

    for key, value in data['iot1/teaching_factory_fast/ground_truth'].items():
        cursor.execute('''
        INSERT INTO ground_truth (id, bottle, is_cracked)
        VALUES (?, ?, ?)
        ''', (int(key), value['bottle'], value['is_cracked']))

    # Commit changes and close connection
    conn.commit()
    conn.close()



if __name__ == '__main__':
    db_file_path = 'teaching_factory.db'
    #json_file_path = 'data.json'


    try:
        create_database(db_file_path)
        print("Database created successfully.")
    except Exception as e:
        print(f"Error: {e}")
        print("Database creation failed.")

    #try:
    #    populate_database(json_file_path, db_file_path)
    #    print("Database populated successfully.")
    #except Exception as e:
    #    print(f"Error: {e}")
    #    print("Database population failed.")