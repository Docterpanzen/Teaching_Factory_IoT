import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

def lade_daten(csv_dateipfad):
    daten = pd.read_csv(csv_dateipfad).dropna()
    daten = daten.loc[:, ~daten.columns.str.contains('^Unnamed')]
    return daten

def trainiere_modell(daten):
    y = daten['final_weight_grams']
    X = daten.drop(columns=['final_weight_grams'])
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    modell = LinearRegression()
    modell.fit(X_train, y_train)
    return modell, X_train, X_test, y_train, y_test

def berechne_mse(modell, X_train, y_train, X_test, y_test):
    y_pred_train = modell.predict(X_train)
    y_pred_test = modell.predict(X_test)
    train_mse = mean_squared_error(y_train, y_pred_train)
    test_mse = mean_squared_error(y_test, y_pred_test)
    return train_mse, test_mse

def berechne_feature_mse(daten):
    feature_mse = {}
    y = daten['final_weight_grams']
    for spalte in daten.columns.drop('final_weight_grams'):
        X = daten[[spalte]]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        modell = LinearRegression()
        modell.fit(X_train, y_train)
        y_pred = modell.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        feature_mse[spalte] = mse
    mse_df = pd.DataFrame.from_dict(feature_mse, orient='index', columns=['MSE'])
    mse_df = mse_df.reset_index().rename(columns={'index': 'Feature'})
    return mse_df

def vorhersage_finalgewicht(modell, zweiter_csv_dateipfad):
    zweite_daten = pd.read_csv(zweiter_csv_dateipfad)
    zweite_daten = zweite_daten.loc[:, ~zweite_daten.columns.str.contains('^Unnamed')]
    vorhersagen = modell.predict(zweite_daten)
    zweite_daten_mit_vorhersagen = zweite_daten.copy()
    zweite_daten_mit_vorhersagen['predicted_final_weight'] = vorhersagen
    return zweite_daten_mit_vorhersagen

def speichere_vorhersagen(daten_mit_vorhersagen, matrikelnummern):
    dateiname = f"reg_{'-'.join(matrikelnummern)}.csv"
    daten_mit_vorhersagen.to_csv(dateiname, index=False)
    return dateiname

# Verwendung der Funktionen
csv_dateipfad = 'data_csv/combined_data.csv'  # Pfad zur ersten CSV-Datei
zweiter_csv_dateipfad = 'data_csv/X.csv'  # Pfad zur zweiten CSV-Datei
matrikelnummern = ['123456', '654321']  # Matrikelnummern der Teilnehmer

# 1. Daten laden
daten = lade_daten(csv_dateipfad)

# 2. Modell trainieren
modell, X_train, X_test, y_train, y_test = trainiere_modell(daten)

# 3. MSE berechnen
train_mse, test_mse = berechne_mse(modell, X_train, y_train, X_test, y_test)
print(f'Train MSE: {train_mse}, Test MSE: {test_mse}')

# 4. Feature MSE berechnen
mse_df = berechne_feature_mse(daten)
print(mse_df)

# 5. Vorhersage für zweite CSV-Datei
zweite_daten_mit_vorhersagen = vorhersage_finalgewicht(modell, zweiter_csv_dateipfad)

# 6. Vorhersagen speichern
dateiname = speichere_vorhersagen(zweite_daten_mit_vorhersagen, matrikelnummern)
print(f'Vorhersagen gespeichert in: {dateiname}')
