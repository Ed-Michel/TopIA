import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.initializers import TruncatedNormal
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split

# Cargar archivo
file_path = "Proyecto_Barcelona/Demanda de agua.csv"

# Cargar datos
data = np.loadtxt(file_path, delimiter=',', skiprows=1)

# Separar datos de entrada y salida
input_data = data[:, 6:7]
output_data = data[:, 6]

# Normalizar tanto los datos de entrada como los de salida
input_scaler = MinMaxScaler()
output_scaler = MinMaxScaler()

trainning_input_normalized = input_scaler.fit_transform(input_data)
trainning_output_normalized = output_scaler.fit_transform(output_data.reshape(-1, 1))

# Dividir los datos en conjuntos de entrenamiento y evaluación (70% - 30%)
trainning_input, evaluation_input, trainning_output, evaluation_output = train_test_split(trainning_input_normalized, trainning_output_normalized, test_size=0.3, random_state=42)

# Método para crear las ventanas de tiempo
def create_time_windows(data, window_size):
    windows = []
    for i in range(len(data) - window_size):
        windows.append(data[i:i+window_size])
    return np.array(windows)

# Definir el tamaño de la ventana de tiempo
window_size = 20 

# Crear ventanas de tiempo para los conjuntos de entrenamiento y evaluación
trainning_input_windows = create_time_windows(trainning_input, window_size)
evaluation_input_windows = create_time_windows(evaluation_input, window_size)

# Aplanar los datos
trainning_input_windows_flat = trainning_input_windows.reshape(trainning_input_windows.shape[0], -1)
evaluation_input_windows_flat = evaluation_input_windows.reshape(evaluation_input_windows.shape[0], -1)

# Arquitectura de la red neuronal
modelo = tf.keras.models.Sequential([
    tf.keras.layers.Dense(units=64, input_shape=(trainning_input_windows_flat.shape[1],), kernel_initializer=TruncatedNormal(mean=0.0, stddev=0.1)),
    tf.keras.layers.Dense(units=128, activation='relu'), 
    tf.keras.layers.Dropout(0.2),  # Agregar dropout para regularización
    tf.keras.layers.Dense(units=64, activation='relu'),
    tf.keras.layers.Dense(units=1)
])

# Compilar el modelo y entrenarlo con las ventanas de tiempo
modelo.compile(
    optimizer=tf.keras.optimizers.Adam(0.001),
    loss='mean_squared_error',
    metrics=['mse']
)

history = modelo.fit(trainning_input_windows, trainning_output[window_size:], epochs=300, batch_size=512, verbose=False)

# Realizar predicciones utilizando el conjunto de datos de evaluación con ventanas de tiempo
predictions_normalized = modelo.predict(evaluation_input_windows_flat)

# Deshacer la normalización de las predicciones de salida
predictions = output_scaler.inverse_transform(predictions_normalized)

# Deshacer la normalización de los datos de evaluación para trazarlos
evaluation_output_original_scale = output_scaler.inverse_transform(evaluation_output).flatten()

plt.plot(evaluation_output_original_scale, label='Actual')
plt.plot(predictions, label='Predicted')
plt.title('Actual vs Predicted')
plt.xlabel('Data Point')
plt.ylabel('Value')
plt.legend()
plt.show()

# Evaluar el modelo con los datos de evaluación con ventanas de tiempo
mse = modelo.evaluate(evaluation_input_windows, evaluation_output[window_size:], verbose=False)[1]
print("MSE del modelo:", mse)

# Graficar el error cuadrático medio durante el entrenamiento
plt.plot(history.history['mse'], label='Training MSE')
plt.title('Model MSE')
plt.xlabel('Epochs')
plt.ylabel('MSE')
plt.legend()
plt.show()