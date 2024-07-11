import sqlite3
import time

def save_dispenser(data):
    conn = sqlite3.connect('data_2.db')
    c = conn.cursor()
    c.execute('''INSERT INTO dispensers (dispenser, bottle, time, fill_level_grams, recipe) 
                 VALUES (?, ?, ?, ?, ?)''', data)
    conn.commit()
    conn.close()

def save_recipe(data):
    conn = sqlite3.connect('data_2.db')
    c = conn.cursor()
    c.execute('''INSERT INTO recipes (recipe, time, red, blue, green) 
                 VALUES (?, ?, ?, ?, ?)''', data)
    conn.commit()
    conn.close()