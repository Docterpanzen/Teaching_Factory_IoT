import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import convert_time as ct

# Function to connect to the database and return the connection and cursor
def connect_to_database():
    conn = sqlite3.connect('teaching_factory.db')
    cur = conn.cursor()
    return conn, cur

# Function to close the database connection
def close_database_connection(conn):
    conn.close()

# Function to fetch data between two datetimes from a specified table and columns
def get_data_from_table(table_name, start_datetime, end_datetime, columns):
    conn, cur = connect_to_database()
    start_datetime_str = start_datetime.strftime('%Y-%m-%d %H:%M:%S')
    end_datetime_str = end_datetime.strftime('%Y-%m-%d %H:%M:%S')
    start_timestamp = ct.convert_readable_to_timestamp(start_datetime_str)
    end_timestamp = ct.convert_readable_to_timestamp(end_datetime_str)
    
    query = f"SELECT {', '.join(columns)} FROM {table_name} WHERE time BETWEEN ? AND ?"
    cur.execute(query, (start_timestamp, end_timestamp))
    rows = cur.fetchall()
    close_database_connection(conn)
    return rows

# Function to fetch data from all dispenser tables between two datetimes
def get_dispenser_data(start_datetime, end_datetime):
    dispenser_columns = ['time', 'fill_level_grams']
    dispenser_red = get_data_from_table('dispenser_red', start_datetime, end_datetime, dispenser_columns)
    dispenser_blue = get_data_from_table('dispenser_blue', start_datetime, end_datetime, dispenser_columns)
    dispenser_green = get_data_from_table('dispenser_green', start_datetime, end_datetime, dispenser_columns)
    return dispenser_red, dispenser_blue, dispenser_green

# Function to fetch final weight data between two datetimes
def get_final_weight_data(start_datetime, end_datetime):
    final_weight_columns = ['time', 'final_weight']
    final_weight = get_data_from_table('final_weight', start_datetime, end_datetime, final_weight_columns)
    return final_weight

# Function to fetch temperature data between two datetimes
def get_temperature_data(start_datetime, end_datetime):
    temperature_columns = ['time', 'temperature_C']
    temperature = get_data_from_table('temperature', start_datetime, end_datetime, temperature_columns)
    return temperature

def display_dispenser_data(data_red, data_blue, data_green, date):
    st.write("Datum: ", date)
    st.divider()
    df_red = pd.DataFrame(data_red, columns=['time', 'fill_level_grams'])
    df_blue = pd.DataFrame(data_blue, columns=['time', 'fill_level_grams'])
    df_green = pd.DataFrame(data_green, columns=['time', 'fill_level_grams'])

    df_red['time'] = df_red['time'].apply(ct.convert_timestamp_to_readable_time)
    df_blue['time'] = df_blue['time'].apply(ct.convert_timestamp_to_readable_time)
    df_green['time'] = df_green['time'].apply(ct.convert_timestamp_to_readable_time)

    st.write("Red Dispenser Data")
    st.write(df_red)
    st.line_chart(df_red.set_index('time').rename(columns={'fill_level_grams': 'Red'}))
    st.divider()
    st.write("Blue Dispenser Data")
    st.write(df_blue)
    st.line_chart(df_blue.set_index('time').rename(columns={'fill_level_grams': 'Blue'}))
    st.divider()
    st.write("Green Dispenser Data")
    st.write(df_green)
    st.line_chart(df_green.set_index('time').rename(columns={'fill_level_grams': 'Green'}))

def display_final_weight_data(data, date):
    st.write("Datum: ", date)
    st.divider()
    df = pd.DataFrame(data, columns=['time', 'final_weight'])
    df['time'] = df['time'].apply(ct.convert_timestamp_to_readable_time)
    st.write(df)
    st.divider()
    st.line_chart(df.set_index('time').rename(columns={'final_weight': 'Final Weight'}))

def display_temperature_data(data, date):
    st.write("Datum: ", date)
    st.divider()
    df = pd.DataFrame(data, columns=['time', 'temperature_C'])
    df['time'] = df['time'].apply(ct.convert_timestamp_to_readable_time)
    st.write(df)
    st.divider()
    st.line_chart(df.set_index('time').rename(columns={'temperature_C': 'Temperature (°C)'}))     


def main():
    st.title("Teaching Factory Dashboard")

    # Sidebar for date selection
    with st.sidebar:
        with st.form("Typ- und Zeitauswahl") as form:
            st.header("Auswahlmenü")
            data_type = st.radio("Wähle eine Option:", ("Dispenser Daten", "Endgewicht Daten", "Temperatur Daten"))
            date = st.date_input("Datum", pd.to_datetime('today') - pd.DateOffset(days=7))
            start_time = st.time_input("Startzeit", pd.Timestamp('00:00:00').time())
            end_time = st.time_input("Endzeit", pd.Timestamp('23:59:59').time())
            start_datetime = pd.to_datetime(str(date) + ' ' + str(start_time))
            end_datetime = pd.to_datetime(str(date) + ' ' + str(end_time))
            submitted_button = st.form_submit_button("Laden")
            if submitted_button:
                if start_datetime >= end_datetime:
                    st.error("Endzeit muss nach der Startzeit liegen.")
                else:
                    st.success("Daten erfolgreich geladen")

    if submitted_button and start_datetime < end_datetime:
        if data_type == "Dispenser Daten":
            st.header("Dispenser Daten")
            data_red, data_blue, data_green = get_dispenser_data(start_datetime, end_datetime)
            if not data_red and not data_blue and not data_green:
                st.error("Keine Daten in der Datenbank für den ausgewählten Zeitraum gefunden.")
                return
            display_dispenser_data(data_red, data_blue, data_green, date)

        elif data_type == "Endgewicht Daten":
            st.header("Endgewicht Daten")
            data = get_final_weight_data(start_datetime, end_datetime)
            if not data:
                st.error("Keine Daten in der Datenbank für den ausgewählten Zeitraum gefunden.")
                return
            display_final_weight_data(data, date)

        elif data_type == "Temperatur Daten":
            st.header("Temperatur Daten")
            data = get_temperature_data(start_datetime, end_datetime)
            if not data:
                st.error("Keine Daten in der Datenbank für den ausgewählten Zeitraum gefunden.")
                return
            display_temperature_data(data, date)

  

if __name__ == "__main__":
    main()
