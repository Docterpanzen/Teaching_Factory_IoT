import sqlite3
import csv

def fetch_all_data(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Fetch all data from dispensers
    cursor.execute("SELECT * FROM dispensers")
    dispensers_data = cursor.fetchall()
    dispensers_headers = [description[0] for description in cursor.description]

    # Fetch all data from recipes
    cursor.execute("SELECT * FROM recipes")
    recipes_data = cursor.fetchall()
    recipes_headers = [description[0] for description in cursor.description]

    conn.close()

    return dispensers_headers, dispensers_data, recipes_headers, recipes_data

def export_to_csv_combined(db_name, csv_file_name):
    dispensers_headers, dispensers_data, recipes_headers, recipes_data = fetch_all_data(db_name)

    # Open the CSV file in append mode
    with open(csv_file_name, mode='a', newline='') as file:
        writer = csv.writer(file)

        # Write headers only if the file is empty
        if file.tell() == 0:
            writer.writerow(dispensers_headers + [""] + recipes_headers)

        # Write data rows
        max_len = max(len(dispensers_data), len(recipes_data))
        for i in range(max_len):
            dispenser_row = list(dispensers_data[i]) if i < len(dispensers_data) else [""] * len(dispensers_headers)
            recipe_row = list(recipes_data[i]) if i < len(recipes_data) else [""] * len(recipes_headers)
            writer.writerow(dispenser_row + [""] + recipe_row)

    print(f"Data exported to {csv_file_name}")

if __name__ == "__main__":
    db_name = 'data.db'          # SQLite database file name
    csv_file_name = 'data.csv'   # Output CSV file name
    export_to_csv_combined(db_name, csv_file_name)
