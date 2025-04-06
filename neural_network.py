import warnings
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
warnings.filterwarnings("ignore") 

import pickle as pc
import numpy as np
from tensorflow.keras.models import Sequential, load_model as keras_load_model
from tensorflow.keras.layers import Dense, Activation
from sklearn.metrics import accuracy_score, mean_absolute_error, mean_squared_error


# Vytváření neuronové sítě
def create_neural_network(input_shape):
    model = Sequential()
    model.add(Dense(30, input_shape=(input_shape,)))
    model.add(Activation('tanh')) 
    model.add(Dense(30))
    model.add(Activation('tanh'))  
    model.add(Dense(1))
    model.add(Activation('linear'))  
    model.compile(loss='mean_squared_error', optimizer='adam', metrics=['mae']) 
    return model

# Trénování modelu 
def train_model_nn(X_train, y_train, X_test, y_test):
    try:
        model = create_neural_network(X_train.shape[1])
        model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=100, batch_size=62, verbose=0)
        return model
    except Exception as e:
        print(f"Chyba při trénování modelu: {str(e)}")
        return None


# Vyhodnocuje neuronovou síť
def evaluate_model_nn(model, X_test, y_test):
    try:
        y_prob = model.predict(X_test).flatten() 
        y_pred = (y_prob > 0.5).astype(int)  
        
        print(f"\nNeuronová Síť:")
        print(f"Přesnost: {accuracy_score(y_test, y_pred)}")
        print(f"Mae: {mean_absolute_error(y_test, y_prob)}")
        print(f"Mse: {mean_squared_error(y_test, y_prob)}") 
    except Exception as e:
        print(f"\nChyba u Neuronové Sítě: {str(e)}")

# Ukládá model neuronové sítě a scaler
def save_model_nn(model, scaler, model_file="dat/nn_model.keras", scaler_file="dat/nn_scaler.pkl"):
    try:
        model.save(model_file)
        with open(scaler_file, "wb") as f:
            pc.dump(scaler, f)
        return True
    except Exception as e:
        print(f"Chyba při ukládání modelu: {str(e)}")
        return False

# Načítá model neuronové sítě a scaler
def load_model_nn(model_file="dat/nn_model.keras", scaler_file="dat/nn_scaler.pkl"):
    try:
        model = keras_load_model(model_file)
        with open(scaler_file, "rb") as f:
            scaler = pc.load(f)
        return model, scaler
    except Exception as e:
        print(f"Chyba při načítání modelu: {str(e)}")
        return None, None
    
# Predikuje výhru na základě modelu neuronové sítě
def predict_win_nn(model, scaler, stats_array):
    try:
        stats_array = np.array(stats_array).reshape(1, -1)
        stats_scaled = scaler.transform(stats_array)
        return model.predict(stats_scaled)[0][0]
    except Exception as e:
        print(f"Chyba při predikci nn: {e}")
        return None
