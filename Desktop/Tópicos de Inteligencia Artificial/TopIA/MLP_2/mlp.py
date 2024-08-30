import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn as sklearn
from sklearn import datasets

from sklearn.model_selection import train_test_split,\
    cross_validate, ShuffleSplit
from sklearn.neural_network import MLPRegressor

from sklearn.preprocessing import StandardScaler

from sklearn.pipeline import Pipeline

from sklearn.metrics import mean_absolute_error,\
    mean_absolute_percentage_error
    
import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))
        
# Para que la división sea random
np.random.seed(306)
cv = ShuffleSplit(n_splits=5, test_size=0.3, random_state=42)

# Se carga el dataset
dataset = sklearn.datasets.fetch_california_housing()
print(dataset.DESCR)

# División 70% y 30% de los datos
X, y = dataset.data, dataset.target

X_train, X_test, y_train, y_test = train_test_split(\
        X, y, test_size=0.3, random_state=1)

# 3 capas ocultas con 32 neuronas
pipe = Pipeline([('scaler', StandardScaler()),
                 ('regressor', MLPRegressor(hidden_layer_sizes=(32)))])

cv_results = cross_validate(pipe,
                           X_train,
                           y_train,
                           cv=cv,
                           scoring="neg_mean_absolute_error",
                           return_train_score=True,
                           return_estimator=True,
                           n_jobs=2)

mlp_train_error = -1 * cv_results['train_score']
mlp_test_error = -1 * cv_results['test_score']

print(f"Mean absolute error of linear regression model on the train set:\n"
      f"{mlp_train_error.mean():.3f} +/- {mlp_train_error.std():.3f}")
print(f"Mean absolute error of linear regression model on the test set:\n"
      f"{mlp_test_error.mean():.3f} +/- {mlp_test_error.std():.3f}")

pipe.fit(X_train, y_train)

# Porcentaje error datos de entrenamiento
mean_absolute_percentage_error(y_train, pipe.predict(X_train))

# Porcentaje error datos de evaluación
mean_absolute_percentage_error(y_test, pipe.predict(X_test))

import matplotlib.pyplot as plt
import numpy as np

# Predicción
y_pred = pipe.predict(X_test)

plt.figure(figsize=(8, 6))

# Gráfico de dispersión con transparencia
plt.scatter(y_test, y_pred, color='blue', alpha=0.5, label='Predicciones')

# Línea de identidad
identity_line = np.linspace(min(y_test), max(y_test), 100)
plt.plot(identity_line, identity_line, 'r--', label='Línea de identidad')

# Etiquetas de los ejes
plt.xlabel('Valores Reales (y_test)')
plt.ylabel('Valores Predichos')
plt.title('Comparación entre Valores Reales y Predichos')
plt.legend()
plt.show()