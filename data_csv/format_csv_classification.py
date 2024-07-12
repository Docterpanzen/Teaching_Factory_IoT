import pandas as pd
import numpy as np
import os

def lade_und_bereite_drop_oscillation_daten_vor(drop_csv_dateipfad, ground_truth_csv_dateipfad, output_directory):
    print(f'Lade Daten von {drop_csv_dateipfad}')
    daten = pd.read_csv(drop_csv_dateipfad)
    
    # Drop Unnamed columns
    daten = daten.loc[:, ~daten.columns.str.contains('^Unnamed')]
    
    # Konvertiere drop_oscillation von string zu Liste von floats
    daten['drop_oscillation'] = daten['drop_oscillation'].apply(lambda x: list(map(float, x.replace('"', '').strip('[]').split(', '))))
    
    # Berechne Merkmale
    daten['mean_drop'] = daten['drop_oscillation'].apply(np.mean)
    daten['std_drop'] = daten['drop_oscillation'].apply(np.std)
    daten['max_drop'] = daten['drop_oscillation'].apply(np.max)
    daten['min_drop'] = daten['drop_oscillation'].apply(np.min)
    
    # Lade ground_truth Daten
    ground_truth_daten = pd.read_csv(ground_truth_csv_dateipfad)
    
    # Drop Unnamed columns
    ground_truth_daten = ground_truth_daten.loc[:, ~ground_truth_daten.columns.str.contains('^Unnamed')]
    
    # Füge is_cracked Informationen hinzu
    daten = daten.merge(ground_truth_daten[['id', 'bottle', 'is_cracked']], on=['id', 'bottle'], how='left')
    
    # Wähle die relevanten Spalten aus
    relevante_spalten = ['id', 'mean_drop', 'std_drop', 'max_drop', 'min_drop', 'is_cracked']
    vorbereitete_daten = daten[relevante_spalten]
    
    # Verzeichnis erstellen, falls nicht vorhanden
    os.makedirs(output_directory, exist_ok=True)
    
    # Pfad zur vorbereiteten CSV-Datei
    vorbereitete_csv_datei = os.path.join(output_directory, 'prepared_drop_oscillation.csv')
    
    # Speichere vorbereitete Daten in eine CSV-Datei
    vorbereitete_daten.to_csv(vorbereitete_csv_datei, index=False)
    
    print(f'Vorbereitete Daten gespeichert in: {vorbereitete_csv_datei}')

# Pfad zu den Daten
drop_csv_dateipfad = 'data_csv/drop_oscillation.csv'
ground_truth_csv_dateipfad = 'data_csv/ground_truth.csv'
output_directory = 'data_csv/'

# 1. Daten laden und vorbereiten
lade_und_bereite_drop_oscillation_daten_vor(drop_csv_dateipfad, ground_truth_csv_dateipfad, output_directory)
