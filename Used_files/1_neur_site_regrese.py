import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

data = pd.read_csv("https://raw.githubusercontent.com/mlcollege/ai-academy/main/06-Regrese/data/ceny_domu.csv", sep=',')
# print(data.head())

input_features = ['kvalita', 'plocha', 'rok_stavby', 'rok_prodeje']
target_feature = 'cena'

X_train, X_test, y_train, y_test = train_test_split(data[input_features], data[target_feature], test_size=0.1, random_state=1)

scaler = StandardScaler()
scaler.fit(X_train)

X_train_std = scaler.transform(X_train)
X_test_std = scaler.transform(X_test)

# print(X_train_std)
# print(X_test_std)

model = Sequential()

model.add(Dense(30, input_shape=(4, )))
model.add(Activation('tanh'))
model.add(Dense(30))
model.add(Activation('tanh'))
model.add(Dense(1))
model.add(Activation('linear'))

model.compile(loss='mean_squared_error',
optimizer='adam',
metrics=['mae'])

model.fit(X_train_std, y_train,
  batch_size = 64, 
  epochs = 100, 
  verbose=1,
  validation_data=(X_test_std, y_test)
)

y_pred = model.predict(X_test_std)

mae= mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)

print("Neuron:")
print(mae)
print(mse)

rf = RandomForestRegressor(n_estimators=50)
rf.fit(X_train, y_train)
y_pred = rf.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)

print("Stromy:")
print(mae)
print(mse)

model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)

print("Lin. regr:")
print(mae)
print(mse)