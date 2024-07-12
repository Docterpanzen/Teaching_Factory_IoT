import pandas as pd
import os

# Dateipfade
data_directory = 'data_csv/'
dispenser_blue_path = os.path.join(data_directory, 'dispenser_blue.csv')
dispenser_green_path = os.path.join(data_directory, 'dispenser_green.csv')
dispenser_red_path = os.path.join(data_directory, 'dispenser_red.csv')
drop_oscillation_path = os.path.join(data_directory, 'drop_oscillation.csv')
final_weight_path = os.path.join(data_directory, 'final_weight.csv')
ground_truth_path = os.path.join(data_directory, 'ground_truth.csv')
recipes_path = os.path.join(data_directory, 'recipes.csv')
temperature_path = os.path.join(data_directory, 'temperature.csv')

# CSV-Dateien einlesen
dispenser_blue = pd.read_csv(dispenser_blue_path)
dispenser_green = pd.read_csv(dispenser_green_path)
dispenser_red = pd.read_csv(dispenser_red_path)
drop_oscillation = pd.read_csv(drop_oscillation_path)
final_weight = pd.read_csv(final_weight_path)
ground_truth = pd.read_csv(ground_truth_path)
recipes = pd.read_csv(recipes_path)
temperature = pd.read_csv(temperature_path)

# Bereinigung der Daten
# Die relevantesten Spalten extrahieren und umbenennen

# Temperaturdaten
temperature_mean = temperature.groupby('id')['temperature_C'].mean().reset_index()
temperature_mean.columns = ['id', 'temperature_mean_C']

# Vibration Index für jede Farbe
vibration_red = dispenser_red[['id', 'vibration_index']]
vibration_red.columns = ['id', 'vibration-index_red_vibration']

vibration_green = dispenser_green[['id', 'vibration_index']]
vibration_green.columns = ['id', 'vibration-index_green_vibration']

vibration_blue = dispenser_blue[['id', 'vibration_index']]
vibration_blue.columns = ['id', 'vibration-index_blue_vibration']

# Fill Level für jede Farbe
fill_level_red = dispenser_red[['id', 'fill_level_grams']]
fill_level_red.columns = ['id', 'fill_level_grams_red']

fill_level_green = dispenser_green[['id', 'fill_level_grams']]
fill_level_green.columns = ['id', 'fill_level_grams_green']

fill_level_blue = dispenser_blue[['id', 'fill_level_grams']]
fill_level_blue.columns = ['id', 'fill_level_grams_blue']

# Zusammenführen der Daten
combined_data = final_weight[['id', 'final_weight']]
combined_data = combined_data.merge(temperature_mean, on='id', how='left')
combined_data = combined_data.merge(vibration_red, on='id', how='left')
combined_data = combined_data.merge(vibration_green, on='id', how='left')
combined_data = combined_data.merge(vibration_blue, on='id', how='left')
combined_data = combined_data.merge(fill_level_red, on='id', how='left')
combined_data = combined_data.merge(fill_level_green, on='id', how='left')
combined_data = combined_data.merge(fill_level_blue, on='id', how='left')

# Entfernen von Zeilen mit fehlenden Werten
combined_data = combined_data.dropna()

# Speichern der bereinigten Daten
cleaned_data_path = os.path.join(data_directory, 'cleaned_combined_data.csv')
combined_data.to_csv(cleaned_data_path, index=False)
print(f"Bereinigte Daten gespeichert in: {cleaned_data_path}")
