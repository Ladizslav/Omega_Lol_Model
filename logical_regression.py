import pickle as pc
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, mean_absolute_error, mean_squared_error

# Trénování modelu 
def train_model_lr(X_train, y_train):
    try:
        model = LogisticRegression(max_iter=1000)
        model.fit(X_train, y_train)
        return model
    except Exception as e:
        print(f"Chyba při trénování modelu: {str(e)}")
        return None

# Vyhodnování modelu 
def evaluate_model_lr(model, X_test, y_test):
    try:
        y_prob = model.predict_proba(X_test)[:, 1] 
        y_pred = model.predict(X_test)
        
        print(f"\nLogistická Regrese:")
        print(f"Přesnost: {accuracy_score(y_test, y_pred)}")
        print(f"Mae: {mean_absolute_error(y_test, y_prob)}")  
        print(f"Mse: {mean_squared_error(y_test, y_prob)}")  
    except Exception as e:
        print(f"\nChyba u Logistické Regrese: {str(e)}")

# Ukládání modelu do dat souboru
def save_model_lr(model, filename="dat/logical_model.dat"):
    try:
        with open(filename, "wb") as f:
            pc.dump(model, f)
        return True
    except Exception as e:
        print(f"Chyba při ukládání modelu: {str(e)}")
        return False

# Načítání modelu z dat souboru
def load_model_lr(filename="dat/logical_model.dat"):
    try:
        with open(filename, "rb") as f:
            return pc.load(f)
    except Exception as e:
        print(f"Chyba při načítání modelu: {str(e)}")
        return None
    
# Predikování výhry
def predict_win_lr(model, stats_df):
    try:
        return model.predict_proba(stats_df)[0][1]
    except Exception as e:
        print(f"Chyba při predikci lr: {e}")
        return None
