import numpy as np
import matplotlib.pyplot as plt
import sklearn as sklearn
import matplotlib.pyplot as plt
import numpy as np

from sklearn.datasets import fetch_california_housing

from sklearn.model_selection import train_test_split,\
    cross_validate, ShuffleSplit
from sklearn.neural_network import MLPRegressor

from sklearn.preprocessing import StandardScaler

from sklearn.pipeline import Pipeline

from sklearn.metrics import mean_absolute_percentage_error
    
import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))
        
# Para que la división sea random
np.random.seed(306)
cv = ShuffleSplit(n_splits=5, test_size=0.3, random_state=42)

# Se carga el dataset
dataset = fetch_california_housing()
print(dataset.DESCR)

# División 70% y 30% de los datos
X, y = dataset.data, dataset.target

X_train, X_test, y_train, y_test = train_test_split(\
        X, y, test_size=0.3, random_state=1)

# 1 capa oculta con 32 neuronas
pipe = Pipeline([('scaler', StandardScaler()),
                 ('regressor', MLPRegressor(hidden_layer_sizes=(32)))])

pipe.fit(X_train, y_train)

# Porcentaje error datos de entrenamiento
mean_absolute_percentage_error(y_train, pipe.predict(X_train))

# Porcentaje error datos de evaluación
mean_absolute_percentage_error(y_test, pipe.predict(X_test))

# Predicción
y_pred = pipe.predict(X_test)

# Crear una nueva figura
plt.figure(figsize=(8, 6))

# Gráfico de dispersión para los valores predichos (azul)
plt.scatter(y_test, y_pred, color='blue', alpha=0.5, label='Predicciones', edgecolor='k')

# Gráfico de dispersión para los valores reales (rojo)
plt.scatter(y_test, y_test, color='red', alpha=0.5, label='Valores Reales', edgecolor='k')

# Etiquetas de los ejes y título
plt.xlabel('Valores Reales (y_test)', fontsize=12)
plt.ylabel('Valores Predichos', fontsize=12)
plt.title('Comparación entre Valores Reales y Predichos', fontsize=14)

# Añadir leyenda y mostrar la gráfica
plt.legend()
plt.show()