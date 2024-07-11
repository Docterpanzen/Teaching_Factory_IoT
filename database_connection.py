import sqlite3

database_file_path = 'teaching_factory.db'

def save_recipe(data):
    conn = sqlite3.connect(database_file_path)
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO recipes (id, recipe, creation_date, red, blue, green)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', data)
    conn.commit()
    conn.close()

def save_final_weight(data):
    conn = sqlite3.connect(database_file_path)
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO final_weight (bottle, time, final_weight)
    VALUES (?, ?, ?)
    ''', data)
    conn.commit()
    conn.close()

def save_drop_oscillation(data):
    conn = sqlite3.connect(database_file_path)
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO drop_oscillation (bottle, drop_oscillation)
    VALUES (?, ?)
    ''', data)
    conn.commit()
    conn.close()

def save_ground_truth(data):
    conn = sqlite3.connect(database_file_path)
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO ground_truth (bottle, is_cracked)
    VALUES (?, ?)
    ''', data)
    conn.commit()
    conn.close()

def save_dispenser_red(data):
    conn = sqlite3.connect(database_file_path)
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO dispenser_red (dispenser, bottle, time, fill_level_grams, recipe, vibration_index)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', data)
    conn.commit()
    conn.close()

def save_dispenser_blue(data):
    conn = sqlite3.connect(database_file_path)
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO dispenser_blue (dispenser, bottle, time, fill_level_grams, recipe, vibration_index)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', data)
    conn.commit()
    conn.close()

def save_dispenser_green(data):
    conn = sqlite3.connect(database_file_path)
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO dispenser_green (dispenser, bottle, time, fill_level_grams, recipe, vibration_index)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', data)
    conn.commit()
    conn.close()

def save_temperature(data):
    conn = sqlite3.connect(database_file_path)
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO temperature (dispenser, time, temperature_C)
    VALUES (?, ?, ?)
    ''', data)
    conn.commit()
    conn.close()
