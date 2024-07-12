import sqlite3

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



if __name__ == '__main__':
    db_file_path = 'teaching_factory.db'


    try:
        create_database(db_file_path)
        print("Database created successfully.")
    except Exception as e:
        print(f"Error: {e}")
        print("Database creation failed.")