import pandas as pd
import numpy as np
import pickle as pc
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import csv

# Načtení a příprava dat
def load_and_prepare_data():
    try:
        data = pd.read_csv("csv/data.csv")
        input_features = ['duration', 'champion_id', 'gold_per_min', 'damage_per_min', 'kda_ratio']
        target_feature = 'win'
        X_train, X_test, y_train, y_test = train_test_split(data[input_features], data[target_feature], test_size=0.2)
        return X_train, X_test, y_train, y_test, input_features      
    except Exception as e:
        print(f"Chyba při přípravě dat: {str(e)}")

# Trénování modelu
def train_model(X_train, y_train):
    try:
        model = LogisticRegression(max_iter=1000)
        model.fit(X_train, y_train)
        return model
    except Exception as e:
        print(f"Chyba při trénování modelu: {str(e)}")

# Vyhodnocení modelu
def evaluate_model(model, X_test, y_test):
    try:
        y_pred = model.predict(X_test)
        presnost = accuracy_score(y_test, y_pred)
        klasifikace = classification_report(y_test, y_pred)
        print(f"Přesnost: {presnost}")
        print(f"Detailní klasifikace: {klasifikace}")
    except Exception as e:
        print(f"Chyba při vyhodnocování modelu: {str(e)}")

# Uložení modelu
def save_model(model):
    try:
        with open("logical_model.dat", "wb") as f:
            pc.dump(model, f)
        print("Vytvořen soubor logical_model.dat")
    except Exception as e:
        print(f"Chyba při ukládání modelu: {str(e)}")

# Příklad predikce
def example_prediction(model, input_features):
    try:
        example_data = pd.DataFrame([[2000, 94, 582.3, 3452.34, 2.38]], columns=input_features)
        win_prob = model.predict_proba(example_data)[0][1]
        prediction = model.predict(example_data)
        
        print("\nPříklad predikce:")
        print(f"Pravděpodobnost výhry: {win_prob:.2%}")
        print(f"Predikovaný výsledek: {'Výhra' if prediction[0] == 1 else 'Prohra'}")
    except Exception as e:
        print(f"Chyba při ukázce predikce: {str(e)}")

# Hlavní část programu
if __name__ == "__main__":
    X_train, X_test, y_train, y_test, input_features = load_and_prepare_data()

    model = train_model(X_train, y_train)
    evaluate_model(model, X_test, y_test)
    save_model(model)
    example_prediction(model, input_features)