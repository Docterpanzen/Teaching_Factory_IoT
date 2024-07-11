import sqlite3

def create_tables():
    conn = sqlite3.connect('data_2.db')
    c = conn.cursor()

    # Create dispensers table
    c.execute('''CREATE TABLE IF NOT EXISTS dispensers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    dispenser TEXT,
                    bottle INTEGER,
                    time INTEGER,
                    fill_level_grams INTEGER,
                    recipe INTEGER
                )''')

    # Create recipes table
    c.execute('''CREATE TABLE IF NOT EXISTS recipes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    recipe TEXT,
                    time INTEGER,
                    red INTEGER,
                    blue INTEGER,
                    green INTEGER
                )''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_tables()
    