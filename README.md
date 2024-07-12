# Teaching Factory
![](images/Teaching_Factory.png)


## Table of Contents
- [Overview](#overview)
- [Installation](#installation)
- [Usage](#usage)
  - [convert_time.py](#convert_timepy)
  - [database.py](#databasepy)
  - [database_connection.py](#database_connectionpy)
  - [mqtt_subscribe.py](#mqtt_subscribepy)
  - [save_data_to_csv.py](#save_data_to_csvpy)
  - [user_interface.py](#user_interfacepy)
  - [visualize.py](#visualizepy)
- [Time Series Data Visualization](#time-series-data-visualization)
- [Streamlit Application](#streamlit-application)
- [Contributing](#contributing)
- [License](#license)

## Overview
The Teaching Factory project is an IoT (Internet of Things) initiative aimed at facilitating data processing, storage, and visualization for industrial applications. This project includes a series of Python scripts designed to handle various aspects of data management, including time conversion, database operations, MQTT communication, and data visualization. The project also features a planned Streamlit web application to provide an interactive interface for data visualization.

### Components:
- *Time Conversion*: Scripts to convert time formats between Unix timestamps and readable date strings.
- *Database Management*: Scripts to create database schemas and manage data insertion.
- *MQTT Communication*: Scripts to subscribe to MQTT topics and save incoming messages to the database.
- *Data Storage*: Scripts to save database tables into CSV files for further analysis.
- *User Interface*: Command-line interface to facilitate user interactions.
- *Data Visualization*: Scripts to plot and visualize data using Plotly.


The project is designed with modularity and scalability in mind, making it easy to integrate additional features and functionalities in the future. The development process involved utilizing various Python libraries and tools to ensure robust and efficient data handling.

## Usage

1. **Clone the Repository**:
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the Streamlit Application**:
    ```bash
    streamlit run user_interface.py
    ```

4. **Run the Visualization Module**:
    ```bash
    python visualize.py
    ```

### convert_time.py
This Python module provides functions to convert between Unix timestamps and readable date strings. It includes functionality to handle user input for conversion and ensure the correct format for timestamps and readable dates.

### database.py
This Python module creates an SQLite database with the necessary tables for the Teaching Factory project. It defines a function to set up the database schema, including tables for recipes, final weight, drop oscillation, ground truth, and dispenser events for red, blue, and green colors, as well as temperature data.

### database_connection.py
This Python module manages saving various types of data to an SQLite database. It defines functions to insert data into different tables including recipes, final weight, drop oscillation, ground truth, and dispenser events for red, blue, and green colors, as well as temperature data.

### mqtt_subscribe.py
This module connects to an MQTT broker, subscribes to various topics related to the teaching factory, and processes the received data to save it into an SQLite database. It utilizes `paho.mqtt.client` for MQTT communication, `json` for parsing the received messages, and a custom `database_connection` module for database operations. The module handles data related to recipes, final weights, drop oscillations, ground truth, dispenser events (for red, blue, and green colors), and temperature.

#### Functions:
- `on_connect(client, userdata, flags, rc, properties=None)`: Connects to the MQTT broker and subscribes to the specified topics.
- `on_message(client, userdata, msg)`: Processes the received messages and saves the data to the database using appropriate functions from the `database_connection` module.

### save_data_to_csv.py
This Python module connects to an SQLite database, extracts data from specified tables, and saves the data as CSV files in a specified directory. It uses sqlite3 for database interaction and pandas for data manipulation and ensures that the data is up-to-date before exporting.

### user_interface.py
This script provides a command-line user interface.

### visualize.py
This Python module connects to an SQLite database, retrieves data from a specified table within a given time range, and visualizes the data as a time series plot. It uses sqlite3 for database interaction, pandas for data manipulation, and plotly.express for plotting, with time conversion utilities provided by the convert_time module.

## Time Series Data Visualization

This Module `visualize.py` fetches and visualizes time series data from an SQLite database using Plotly. It includes functions for converting timestamps, querying data, and plotting it in a line chart. Below are example plots for `final_weight` and `temperature` data, demonstrating the script's capability to generate insightful visualizations from the database.


### Final Weight Plot
![Final Weight Plot](images/Plot_Final_Weight.jpg)
*Final weight data visualization.*

### Temperature Plot
![Temperature Plot](images/Plot_Temperature.jpg)
*Temperature data visualization.*


## Streamlit Application
The Streamlit application `user_interface.py` provides an interface to visualize time series data from an SQLite database. Users can select data types and time ranges to view data in tabular and line chart formats. The application includes error handling for invalid date ranges and uses a loading spinner to simulate data fetching delays.

### Features

- **Date and Time Selection**: Users can select a specific date and time range to fetch data.
- **Data Type Selection**: Users can choose between different data types: Dispenser Data, Final Weight Data, and Temperature Data.
- **Data Fetching**: Fetches data from an SQLite database based on user selection.
- **Data Visualization**: Displays data in a table format and as a line chart using Plotly.
- **Error Handling**: Provides error messages for invalid date ranges and when no data is found.
- **Loading Spinner**: Displays a spinner while data is being fetched.


