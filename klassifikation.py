import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, confusion_matrix

def lade_drop_vibration_daten(csv_dateipfad):
    print(f'Lade Daten von {csv_dateipfad}')
    daten = pd.read_csv(csv_dateipfad)
    daten = daten.loc[:, ~daten.columns.str.contains('^Unnamed')]
    print(f"Vorhandene Spalten: {daten.columns.tolist()}")
    print(f"Erste Zeilen der Daten:\n{daten.head()}")
    return daten

def erstelle_klassifikationsmodell(daten, ergebnis_csv_pfad, confusion_matrix_pfad):
    print('Erstelle Klassifikationsmodell')
    X = daten.drop(columns=['is_cracked', 'id'])
    y = daten['is_cracked']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    modelle = {
        'kNN': KNeighborsClassifier(),
        'Log. Regression': LogisticRegression(max_iter=1000)
    }
    
    ergebnisse = []
    confusion_matrices = {}
    
    for name, model in modelle.items():
        model.fit(X_train, y_train)
        y_pred_train = model.predict(X_train)
        y_pred_test = model.predict(X_test)
        
        f1_train = f1_score(y_train, y_pred_train)
        f1_test = f1_score(y_test, y_pred_test)
        
        ergebnisse.append({
            'Genutzte Features': X.columns.tolist(),
            'Modell-Typ': name,
            'F1-Score (Training)': f1_train,
            'F1-Score (Test)': f1_test
        })
        
        cm = confusion_matrix(y_test, y_pred_test)
        confusion_matrices[name] = cm
        print(f"Confusion Matrix for {name}:\n{cm}")
    
    ergebnis_df = pd.DataFrame(ergebnisse)
    
    # Ergebnisse speichern
    ergebnis_df.to_csv(ergebnis_csv_pfad, index=False)
    print(f'Ergebnisse gespeichert in: {ergebnis_csv_pfad}')
    
    # Confusion Matrix speichern
    with open(confusion_matrix_pfad, 'w') as f:
        for name, cm in confusion_matrices.items():
            f.write(f'Confusion Matrix for {name}:\n{cm}\n\n')
    print(f'Confusion Matrices gespeichert in: {confusion_matrix_pfad}')
    
    return ergebnis_df, confusion_matrices

# Pfad zu den Daten
csv_dateipfad = 'data_csv/prepared_drop_oscillation.csv'
ergebnis_csv_pfad = 'klassifikations_ergebnisse.csv'
confusion_matrix_pfad = 'confusion_matrices.txt'

# 1. Daten laden
daten = lade_drop_vibration_daten(csv_dateipfad)

# 2. Klassifikationsmodell erstellen und evaluieren
ergebnisse, confusion_matrices = erstelle_klassifikationsmodell(daten, ergebnis_csv_pfad, confusion_matrix_pfad)

# 3. Ergebnisse ausgeben
print('Ergebnisse der Klassifikation:')
print(ergebnisse)
