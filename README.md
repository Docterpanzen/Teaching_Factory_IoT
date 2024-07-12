# Teaching Factory

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
- [Streamlit Application](#streamlit-application)
- [Contributing](#contributing)
- [License](#license)

## Overview
The Teaching Factory project is an IoT (Internet of Things) initiative aimed at facilitating data processing, storage, and visualization for industrial applications. This project includes a series of Python scripts designed to handle various aspects of data management, including time conversion, database operations, MQTT communication, and data visualization. The project also features a planned Streamlit web application to provide an interactive interface for data visualization.

### Components:
- *Time Conversion*: Scripts to convert time formats between Unix timestamps and readable date strings..
- *Database Management*: Scripts to create database schemas, manage connections, and handle data insertion.
- *MQTT Communication*: Scripts to subscribe to MQTT topics and process incoming messages.
- *Data Storage*: Scripts to save data into CSV files for further analysis.
- *User Interface*: Command-line interface for user interaction.
- *Data Visualization*: Scripts to plot and visualize data using matplotlib.

The project is designed with modularity and scalability in mind, making it easy to integrate additional features and functionalities in the future. The development process involved utilizing various Python libraries and tools to ensure robust and efficient data handling.

## Usage

1. Clone the repository:
   bash
   git clone https://github.com/Docterpanzen/Teaching_Factory_IoT.git
   

2. Navigate to the project directory:
    bash
    cd Teaching_Factory_IoT
    

3. Install the required packages:
    bash
    pip install -r requirements.txt
    

### convert_time.py
This script is used to convert time formats.

### database.py

Creat the database with all the tables.

### database_connection.py
This script manages the database connection, facilitating the saving of data received from MQTT into the database.

### mqtt_subscribe.py
This script subscribes to MQTT topics and processes incoming messages. It saves the Data with help from the functions in database_connection.py

### save_data_to_csv.py
This script saves data from the Database to seperate CSV files and a combined_data CSV file.

### user_interface.py
This script provides a command-line user interface.

### visualize.py
This script is used to visualize data.


## Plots

### Final Weight Plot
![Final Weight Plot](images/Plot_Final_Weight.jpg)

### Temperature Plot
![Temperature Plot](images/PlotTemperature.jpg)


## Streamlit Application
A Streamlit application is planned to visualize the data in a web interface. This feature is currently under development and will provide an interactive and user-friendly way to explore and analyze the collected data.

## Contributing
Contributions are welcome! Please read the [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on contributing to this project.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
