import sqlite3
import pandas as pd
import plotly.express as px
import convert_time as ct

def fetch_data_from_db(db_file_path, table_name, time_column, value_column, start_time, end_time):
    conn = sqlite3.connect(db_file_path)
    query = f"""
    SELECT {time_column}, {value_column} FROM {table_name}
    WHERE {time_column} BETWEEN {start_time} AND {end_time}
    ORDER BY {time_column}
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def plot_time_series(df, time_column, value_column, title):
    fig = px.line(df, x=time_column, y=value_column, title=title)
    fig.show()

def main(db_file_path, table_name, time_column, value_column, start_time, end_time):
    # Convert readable date to timestamp if necessary
    if isinstance(start_time, str):
        start_time = ct.convert_readable_to_timestamp(start_time)
    if isinstance(end_time, str):
        end_time = ct.convert_readable_to_timestamp(end_time)
    
    df = fetch_data_from_db(db_file_path, table_name, time_column, value_column, start_time, end_time)
    
    # Convert timestamp to readable date for plotting
    df[time_column] = df[time_column].apply(ct.convert_timestamp_to_readable)
    
    plot_time_series(df, time_column, value_column, f"Time Series of {value_column} from {table_name}")

if __name__ == '__main__':
    # Configuration
    db_file_path = 'teaching_factory.db'  # Replace with your actual database file path
    table_name = 'temperature'            # Replace with the table you want to visualize
    time_column = 'time'                  # Replace with the time column in the table
    value_column = 'temperature_C'        # Replace with the value column you want to plot
    start_time = '2024-07-11 22:41:00'    # Replace with the start time (readable date)
    end_time = '2024-07-12 00:15:00'      # Replace with the end time (readable date)
    # keep the time between 2024-07-11 22:41:00 and 2024-07-12 00:15:00

    main(db_file_path, table_name, time_column, value_column, start_time, end_time)
