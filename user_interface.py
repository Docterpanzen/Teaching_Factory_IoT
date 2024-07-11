import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# Function to connect to the database and return the connection and cursor
def connect_to_database():
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    return conn, cur

# Function to close the database connection
def close_database_connection(conn):
    conn.close()

# Function to fetch dispenser data between two datetimes
def get_dispenser_data(start_datetime, end_datetime):
    conn, cur = connect_to_database()
    start_timestamp = int(start_datetime.timestamp())
    end_timestamp = int(end_datetime.timestamp())
    
    query = "SELECT * FROM dispensers WHERE time BETWEEN ? AND ?"
    cur.execute(query, (start_timestamp, end_timestamp))
    rows = cur.fetchall()
    close_database_connection(conn)
    return rows

# Function to fetch recipe data between two datetimes
def get_recipe_data(start_datetime, end_datetime):
    conn, cur = connect_to_database()
    start_timestamp = int(start_datetime.timestamp())
    end_timestamp = int(end_datetime.timestamp())
    
    query = "SELECT * FROM recipes WHERE time BETWEEN ? AND ?"
    cur.execute(query, (start_timestamp, end_timestamp))
    rows = cur.fetchall()
    close_database_connection(conn)
    return rows

def main():
    st.title("Teaching Factory Dashboard")

    # Sidebar for date selection
    with st.sidebar:
        st.header("Select Data and Time Range")
        data_type = st.radio("Choose Data Type:", ("Dispenser Data", "Recipe Data"))
        date = st.date_input("Select Date", datetime.now().date())
        start_time = st.time_input("Start Time", datetime.now().time())
        end_time = st.time_input("End Time", datetime.now().time())
        start_datetime = datetime.combine(date, start_time)
        end_datetime = datetime.combine(date, end_time)
        submitted_button = st.button("Fetch Data")

    if submitted_button:
        if data_type == "Dispenser Data":
            st.header("Dispenser Data")
            data = get_dispenser_data(start_datetime, end_datetime)
            df = pd.DataFrame(data, columns=['id', 'dispenser', 'bottle', 'time', 'fill_level_grams', 'recipe'])
            df['time'] = pd.to_datetime(df['time'], unit='s')
            st.write(df)
            st.line_chart(df.set_index('time')['fill_level_grams'])

        elif data_type == "Recipe Data":
            st.header("Recipe Data")
            data = get_recipe_data(start_datetime, end_datetime)
            df = pd.DataFrame(data, columns=['id', 'recipe', 'time', 'red', 'blue', 'green'])
            df['time'] = pd.to_datetime(df['time'], unit='s')
            st.write(df)
            st.line_chart(df.set_index('time')[['red', 'blue', 'green']])

if __name__ == "__main__":
    main()
    time_test = pd.to_datetime(1718711822, unit='s')
    print(time_test)