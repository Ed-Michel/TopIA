# importar librerías y cargar el dataset
import numpy as np
np.random.seed(4)
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM

dataset = pd.read_csv('sample_data/AAPL_2006-01-01_to_2018-01-01.csv', index_col='Date', parse_dates=['Date'])
dataset.head()

# división 90% (entrenamiento) y 10% (evaluación)
set_entrenamiento = dataset[:'2016'].iloc[:,1:2]
set_evaluacion = dataset['2017':].iloc[:,1:2]

# normalización de los datos de entrenamiento
sc = MinMaxScaler(feature_range=(0,1))
set_entrenamiento_escalado = sc.fit_transform(set_entrenamiento)

# ventanas de tiempo (por cada 60 datos, se predice el siguiente valor [61])
time_step = 60
X_train = []
Y_train = []
m = len(set_entrenamiento_escalado)

for i in range(time_step,m):
    # X: bloques de "time_step" datos: 0-time_step, 1-time_step+1, 2-time_step+2, etc
    X_train.append(set_entrenamiento_escalado[i-time_step:i,0])

    # Y: el siguiente dato
    Y_train.append(set_entrenamiento_escalado[i,0])
X_train, Y_train = np.array(X_train), np.array(Y_train)

plt.figure(figsize=(14, 8))

# graficar la serie de tiempo original
plt.plot(range(m), set_entrenamiento_escalado, color='blue', label='Serie de tiempo original')

# graficar los valores predichos (Y_train), desplazados para que coincidan con los valores reales
plt.plot(range(time_step, m), Y_train, color='red', label='Valores predichos (Y_train)')

plt.xlabel('Tiempo')
plt.ylabel('Valor')
plt.title('Serie de Tiempo con Predicciones usando Ventanas de Tiempo')
plt.legend()
plt.show()

# ajustes antes de crear la LSTM (vectores 60x1)
X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

# creación de la red LSTM (capa de entrada, 50 neuronas y capa de salida)
dim_entrada = (X_train.shape[1],1)
dim_salida = 1
neuronas = 50

# contenedor
modelo = Sequential()

modelo.add(LSTM(units=neuronas, input_shape=dim_entrada))
modelo.add(Dense(units=dim_salida))

# compilación del modelo (función de pérdida: error cuadrático medio || optimizador: gradiente descendiente)
modelo.compile(optimizer='rmsprop', loss='mse')

# entrenamiento (20 épocas y lotes de 32 datos)
modelo.fit(X_train,Y_train,epochs=20,batch_size=32)

# normalización de los datos de evaluación
x_test = set_evaluacion.values
x_test = sc.transform(x_test)

# reorganización de bloques de 60 datos
X_test = []
for i in range(time_step,len(x_test)):
    X_test.append(x_test[i-time_step:i,0])
X_test = np.array(X_test)
X_test = np.reshape(X_test, (X_test.shape[0],X_test.shape[1],1))

# realizar predicciones y graficarlas
prediccion = modelo.predict(X_test)
prediccion = sc.inverse_transform(prediccion)

plt.plot(set_evaluacion.values[0:len(prediccion)],color='red', label='Valor real de la acción')
plt.plot(prediccion, color='blue', label='Predicción de la acción')
plt.ylim(1.1 * np.min(prediccion)/2, 1.1 * np.max(prediccion))
plt.xlabel('Tiempo')
plt.ylabel('Valor de la acción')
plt.legend()
plt.show()