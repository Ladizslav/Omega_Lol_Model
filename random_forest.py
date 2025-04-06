import pickle as pc
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, mean_absolute_error, mean_squared_error

# Trénování modelu 
def train_model_rf(X_train, y_train):
    try:
        model = RandomForestClassifier(n_estimators=100, max_depth=5)
        model.fit(X_train, y_train)
        return model
    except Exception as e:
        print(f"Chyba při trénování modelu: {str(e)}")
        return None

# Vyhodnování modelu 
def evaluate_model_rf(model, X_test, y_test):
    try:
        y_prob = model.predict_proba(X_test)[:, 1] 
        y_pred = model.predict(X_test)
        print(f"\nRandom Forest:")
        print(f"Přesnost: {accuracy_score(y_test, y_pred)}")
        print(f"Mae: {mean_absolute_error(y_test, y_prob)}")
        print(f"Mse: {mean_squared_error(y_test, y_prob)}")
    except Exception as e:
        print(f"\nChyba u Random Forestu: {str(e)}")

# Ukládání modelu do dat souboru
def save_model_rf(model, filename="dat/random_forest_model.dat"):
    try:
        with open(filename, "wb") as f:
            pc.dump(model, f)
        return True
    except Exception as e:
        print(f"Chyba při ukládání modelu: {str(e)}")
        return False

# Načítání modelu z dat souboru
def load_model_rf(filename="dat/random_forest_model.dat"):
    try:
        with open(filename, "rb") as f:
            return pc.load(f)
    except Exception as e:
        print(f"Chyba při načítání modelu: {str(e)}")
        return None
    
# Predikování výhry
def predict_win_rf(model, stats_df):
    try:
        return model.predict_proba(stats_df)[0][1]
    except Exception as e:
        print(f"Chyba při predikci rf: {e}")
        return None
