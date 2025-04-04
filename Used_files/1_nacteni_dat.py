import pandas as pd
import numpy as np
import pickle as pc
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error

data = pd.read_csv("https://raw.githubusercontent.com/mlcollege/ai-academy/main/06-Regrese/data/ceny_domu.csv", sep=',')
### 1.
#print(data.columns)
#print(data.head(5))

### 2.
input_features = ['kvalita', 'plocha', 'rok_stavby',  'rok_prodeje']
target_feature = 'cena'

X_train, X_test, y_train, y_test = train_test_split(data[input_features], data[target_feature], test_size=0.1)

# pro rozdělení na 80/20
# větší chybovost
#X_train, X_test, y_train, y_test = train_test_split(data[input_features], data[target_feature], test_size=0.2)


# print(X_train)
# print(X_test)
# print(y_train)
# print(y_test)

### 3.
model = LinearRegression()
model.fit(X_train, y_train)

#print (model.coef_) #koeficienty vstupnich atributu
#print (model.intercept_) #konstantni posuv linearni kombinace

### 4.

y_pred = model.predict(X_test)

#print(y_test.head(10).values)
#print(y_pred[:10])

chyba = np.abs(y_test.head(10).values-y_pred[:10])
#print(chyba)

### 5.

mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)

print(mae)
print(mse)

### 6. 

with open("muj_model.dat", "wb") as f:
    pc.dump(model, f)

with open("muj_model.dat", "rb") as f:
    model = pc.load(f)

atributy_domu = np.array([[8, 140, 2003, 2020]]) 
predikovana_cena = model.predict(atributy_domu)
print(f"{predikovana_cena[0]} mil. kč")


