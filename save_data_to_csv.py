import sqlite3
import pandas as pd
import os

def save_table_to_csv(cursor, table_name, directory):
    # Fetch all data from the table
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()

    # Get column names
    column_names = [description[0] for description in cursor.description]

    # Convert to DataFrame
    df = pd.DataFrame(rows, columns=column_names)

    # Create directory if it doesn't exist
    os.makedirs(directory, exist_ok=True)

    # Save DataFrame to CSV
    csv_path = os.path.join(directory, f"{table_name}.csv")
    df.to_csv(csv_path, index=False)

def export_db_to_csv(db_file_path, output_directory):
    # Connect to the database
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()

    # List of tables to export
    tables = [
        'recipes',
        'final_weight',
        'drop_oscillation',
        'ground_truth',
        'dispenser_red',
        'dispenser_blue',
        'dispenser_green',
        'temperature'
    ]

    # Export each table to CSV
    for table in tables:
        save_table_to_csv(cursor, table, output_directory)
    

    # Close the connection
    conn.close()

# Specify the database file path and output directory
db_file_path = 'teaching_factory.db'  # replace with your actual database file path
output_directory = 'data_csv/'


if __name__ == '__main__':
    try:
        # Export the database tables to CSV
        export_db_to_csv(db_file_path, output_directory)
        print(f"Database tables exported to CSV files in '{output_directory}' directory.")
    except Exception as e:
        print(f"Error: {e}")
