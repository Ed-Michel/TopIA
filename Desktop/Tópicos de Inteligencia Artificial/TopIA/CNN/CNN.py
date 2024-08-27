import os
import cv2
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from tensorflow.keras import layers, models
import matplotlib.pyplot as plt

# Función para cargar y procesar imágenes
def cargar_imagenes_y_procesar(ruta):
    imagenes = []
    etiquetas = []

    for filename in os.listdir(ruta):
        img_path = os.path.join(ruta, filename)
        
        # Intentar cargar la imagen
        try:
            img = cv2.imread(img_path)
            if img is None:
                print(f"Error: No se pudo cargar la imagen {img_path}")
                continue
        except Exception as e:
            print(f"Error al cargar la imagen {img_path}: {e}")
            continue

        # Intentar redimensionar y normalizar la imagen
        try:
            img = cv2.resize(img, (100, 100))  # Redimensionar la imagen
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convertir a escala de grises
            img = img / 255.0  # Normalizar los valores de píxeles
        except Exception as e:
            print(f"Error al redimensionar la imagen {img_path}: {e}")
            continue

        imagenes.append(img)  # Agregar la imagen a la lista
        etiquetas.append(float(filename.split("_")[1].split(".")[0]))  # Extraer la etiqueta de la imagen

    return np.array(imagenes), np.array(etiquetas)

# Ruta de la carpeta de imágenes
folder_path = "Proyecto_CNN_Algas/PRACTICA_ALGAS/IMAGENES"

# Cargar y procesar las imágenes
X, y = cargar_imagenes_y_procesar(folder_path)

# Verificar si se cargaron correctamente las imágenes
if len(X) == 0 or len(y) == 0:
    print("No se encontraron imágenes válidas en la carpeta.")
    exit()

# Separar los datos en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Normalizar las etiquetas de salida con MinMaxScaler
scaler_y = MinMaxScaler()
y_train_normalized = scaler_y.fit_transform(y_train.reshape(-1, 1)).flatten()
y_test_normalized = scaler_y.transform(y_test.reshape(-1, 1)).flatten()

# Definir el modelo CNN
model = models.Sequential([
    layers.Conv2D(64, (5, 5), activation='relu', input_shape=(100, 100, 1)),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(128, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(128, (3, 3), activation='relu'),
    layers.Flatten(),
    layers.Dense(100, activation='relu'),
    layers.Dense(50, activation='relu'),
    layers.Dense(1)
])

# Compilar el modelo
model.compile(optimizer='adam', loss='mse')

# Entrenar el modelo
history = model.fit(X_train[..., np.newaxis], y_train_normalized, epochs=500, validation_split=0.2)

# Evaluar el modelo en el conjunto de prueba
mse_test = model.evaluate(X_test[..., np.newaxis], y_test_normalized)

# Obtener las predicciones del modelo en el conjunto de prueba
predicciones_modelo_test = model.predict(X_test[..., np.newaxis]).flatten()

# Calcular el error cuadrático medio entre las predicciones del modelo y las etiquetas reales en el conjunto de prueba
print("Mean Squared Error (MSE) entre las predicciones del modelo y las etiquetas reales (conjunto de prueba):", mse_test)

# Desnormalizar las etiquetas predichas y las etiquetas reales para la visualización
predicciones_modelo_test_desnormalized = scaler_y.inverse_transform(predicciones_modelo_test.reshape(-1, 1)).flatten()
y_test_desnormalized = scaler_y.inverse_transform(y_test_normalized.reshape(-1, 1)).flatten()

# Mostrar la gráfica de comparación entre las etiquetas reales y las predicciones del modelo en el conjunto de prueba
plt.scatter(y_test_desnormalized, predicciones_modelo_test_desnormalized, c='blue', label='Predicciones del modelo (conjunto de prueba)')
plt.scatter(y_test_desnormalized, y_test_desnormalized, c='red', label='Datos reales del archivo Excel (conjunto de prueba)')
plt.xlabel("Biomasa real (g/L)")
plt.ylabel("Biomasa estimada (g/L)")
plt.title("Comparación entre la biomasa real y la estimada por el modelo (conjunto de prueba)")
plt.legend()
plt.show()
