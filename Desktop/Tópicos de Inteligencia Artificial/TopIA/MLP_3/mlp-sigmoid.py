import pandas as pd
import numpy as np
from PIL import Image

# Cargar el dataset
data = pd.read_csv("sample_data/mnist.csv")

# Separar las etiquetas y las características
X = data.iloc[:, 1:].values  # Características (píxeles)
y = data.iloc[:, 0].values   # Etiquetas (dígitos)

# Normalizar los valores de los píxeles
X = X / 255.0

# Codificación one-hot de las etiquetas
y_one_hot = np.zeros((y.size, y.max() + 1))
y_one_hot[np.arange(y.size), y] = 1

# Verificar los tamaños
print("Tamaño de X:", X.shape)  # Debería ser (n_samples, 784)
print("Tamaño de y (one-hot):", y_one_hot.shape)  # Debería ser (n_samples, 10)

# Función de activación sigmoide
def sigmoid(x):
    x = np.clip(x, -500, 500)  # Limitar los valores a un rango razonable
    return 1 / (1 + np.exp(-x))

def relu(x):
    return np.maximum(0, x)

def relu_derivative(x):
    return np.where(x > 0, 1, 0)

# Pérdida de entropía cruzada
def cross_entropy_loss(y_true, y_pred):
    n_samples = y_true.shape[0]
    y_pred_clipped = np.clip(y_pred, 1e-9, 1 - 1e-9)
    return -np.sum(y_true * np.log(y_pred_clipped)) / n_samples

# Derivada de la pérdida
def cross_entropy_derivative(y_true, y_pred):
    return y_pred - y_true

# Clase de la red neuronal con sigmoid en la salida
class MLP_Sigmoid:
    def __init__(self, input_size, hidden_size, output_size):
        # Inicializamos pesos y sesgos
        self.W1 = np.random.randn(input_size, hidden_size) * 0.01
        self.b1 = np.zeros((1, hidden_size))
        self.W2 = np.random.randn(hidden_size, output_size) * 0.01
        self.b2 = np.zeros((1, output_size))

    def forward(self, X):
        # Capa oculta
        self.z1 = np.dot(X, self.W1) + self.b1
        self.a1 = relu(self.z1)

        # Capa de salida con sigmoid
        self.z2 = np.dot(self.a1, self.W2) + self.b2
        self.a2 = sigmoid(self.z2)

        return self.a2

    def backpropagation(self, X, y_true, learning_rate=0.01):
        # Propagación hacia atrás (backpropagation)
        n_samples = X.shape[0]

        # Derivada de la capa de salida
        dz2 = cross_entropy_derivative(y_true, self.a2)
        dW2 = np.dot(self.a1.T, dz2) / n_samples
        db2 = np.sum(dz2, axis=0, keepdims=True) / n_samples

        # Derivadas de la capa oculta (ReLU)
        dz1 = np.dot(dz2, self.W2.T) * relu_derivative(self.z1)
        dW1 = np.dot(X.T, dz1) / n_samples
        db1 = np.sum(dz1, axis=0, keepdims=True) / n_samples

        # Actualizamos los pesos y sesgos
        self.W2 -= learning_rate * dW2
        self.b2 -= learning_rate * db2
        self.W1 -= learning_rate * dW1
        self.b1 -= learning_rate * db1

    def train(self, X, y_true, epochs=1000, learning_rate=0.01):
        for epoch in range(epochs):
            # Forward pass
            y_pred = self.forward(X)

            # Calculamos la pérdida
            loss = cross_entropy_loss(y_true, y_pred)

            # Backward pass
            self.backpropagation(X, y_true, learning_rate)

            if epoch % 100 == 0:
                print(f'Epoch {epoch}, Loss: {loss}')
                
# Inicializar y entrenar el MLP
mlp = MLP_Sigmoid(input_size=784, hidden_size=128, output_size=10)  # 784 entradas, 128 neuronas ocultas, 10 salidas
mlp.train(X, y_one_hot, epochs=1000, learning_rate=0.01)

# Preprocesamiento para la predicción de imágenes del mundo real
def preprocess_image(image_path):
    # Cargar la imagen desde un archivo
    image = Image.open(image_path).convert('L')  # Convertir a escala de grises

    # Redimensionar a 28x28 píxeles (tamaño del dataset MNIST)
    image = image.resize((28, 28))

    # Convertir la imagen a una matriz numpy y normalizar los valores de los píxeles (0-255 -> 0-1)
    image_array = np.array(image) / 255.0

    # Aplanar la imagen en un vector de 784 valores (28x28)
    image_flattened = image_array.flatten().reshape(1, -1)

    return image_flattened

# Cargar y preprocesar la imagen
image_flattened = preprocess_image("sample_data/0.png")

# Usar el modelo MLP para hacer la predicción
prediccion = mlp.forward(image_flattened)

# Mostrar la predicción
print("Predicción:", np.argmax(prediccion))  # np.argmax te dará la clase con mayor probabilidad