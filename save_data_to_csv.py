import sqlite3
import pandas as pd
import os

def save_table_to_csv(cursor, table_name, directory):
    # Get all the data from the table
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()

    # Get the column names
    column_names = [description[0] for description in cursor.description]

    # Convert the data to a pandas DataFrame
    df = pd.DataFrame(rows, columns=column_names).drop_duplicates().reset_index(drop=True)

    # Make sure the directory exists
    os.makedirs(directory, exist_ok=True)

    # Path to the CSV file
    csv_path = os.path.join(directory, f"{table_name}.csv")

    if os.path.exists(csv_path):
        # Read the existing data
        existing_df = pd.read_csv(csv_path).drop_duplicates().reset_index(drop=True)

        # Ensure the columns are in the same order
        df = df[existing_df.columns]

        # Convert data types to match
        df = df.astype(existing_df.dtypes.to_dict())

        # Sort DataFrames for accurate comparison
        df = df.sort_values(by=list(df.columns)).reset_index(drop=True)
        existing_df = existing_df.sort_values(by=list(existing_df.columns)).reset_index(drop=True)

        if existing_df.equals(df):
            print(f"{table_name}.csv is already up to date.")
            return df, False

    # Save the DataFrame to a CSV file
    df.to_csv(csv_path, index=False)
    print(f"{table_name}.csv has been updated.")
    return df, True

def export_db_to_csv(db_file_path, output_directory):
    # Connect to the database
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()

    # List of tables we want to export
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

    # This will hold all the data combined
    combined_df = pd.DataFrame()
    updated = False

    # Export each table to its own CSV and add it to the combined DataFrame
    for table in tables:
        df, is_updated = save_table_to_csv(cursor, table, output_directory)
        if is_updated:
            updated = True
        df['source_table'] = table  # Add a column to show which table the data came from
        combined_df = pd.concat([combined_df, df], ignore_index=True).drop_duplicates().reset_index(drop=True)

    # Path to the combined CSV file
    combined_csv_path = os.path.join(output_directory, "combined_data.csv")

    if os.path.exists(combined_csv_path):
        # Read the existing combined data
        existing_combined_df = pd.read_csv(combined_csv_path).drop_duplicates().reset_index(drop=True)

        # Ensure the columns are in the same order
        combined_df = combined_df[existing_combined_df.columns]

        # Convert data types to match
        combined_df = combined_df.astype(existing_combined_df.dtypes.to_dict())

        # Sort DataFrames for accurate comparison
        combined_df = combined_df.sort_values(by=list(combined_df.columns)).reset_index(drop=True)
        existing_combined_df = existing_combined_df.sort_values(by=list(existing_combined_df.columns)).reset_index(drop=True)

        if existing_combined_df.equals(combined_df) and not updated:
            print(f"combined_data.csv is already up to date.")
            return

    # Save the combined DataFrame to a single CSV file
    combined_df.to_csv(combined_csv_path, index=False)
    print("combined_data.csv has been updated.")

    # Close the database connection
    conn.close()

# Set the database file path and output directory
db_file_path = 'teaching_factory.db'  # replace with your actual database file path
output_directory = 'data_csv/'

if __name__ == '__main__':
    try:
        # Run the export function
        export_db_to_csv(db_file_path, output_directory)
        print(f"Database tables exported to CSV files in '{output_directory}' directory.")
    except Exception as e:
        print(f"Error: {e}")
