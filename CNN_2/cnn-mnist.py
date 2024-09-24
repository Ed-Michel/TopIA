from PIL import Image, ImageEnhance
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras import layers, models
import tensorflow as tf

# cargar el conjunto de datos MNIST
mnist = tf.keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# dado que una CNN trabaja con canales RGB, los vectores con los que estamos trabajando necesitan ser adecuados a la red
# (MNIST está en una escala de grises)
x_train = x_train.reshape(-1, 28, 28, 1)
x_test = x_test.reshape(-1, 28, 28, 1)

# normalización de los datos
x_train = x_train.astype("float32")/255
x_test = x_test.astype("float32")/255

# se define la CNN
model = models.Sequential()
model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))

# añadir capas densas para clasificación
model.add(layers.Flatten())
model.add(layers.Dense(128, activation='relu'))
model.add(layers.Dense(10, activation='softmax'))  # 10 clases (0-9)

# compilación del modelo
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=["accuracy"])

# entrenamiento de la red CNN
batch_size = 64
epochs = 5

history = model.fit(x_train, y_train, batch_size=batch_size, epochs=epochs,
                    validation_data=(x_test, y_test), verbose=1)

# evaluar el modelo
test_loss, test_acc = model.evaluate(x_test, y_test)
print(f'Pérdida en el conjunto de prueba: {test_loss}')
print(f'Precisión en el conjunto de prueba: {test_acc}')

# gráfica del performance del modelo
plt.figure(figsize=(13, 5))
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend(['Train','Test'])
plt.grid()
plt.show()

def preprocess_image(image_path):
    # abrir la imagen y convertirla a escala de grises
    img = Image.open(image_path).convert('L')

    # mejorar el contraste de la imagen si es necesario
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2)  # incrementa el contraste por un factor de 2

    # redimensionar la imagen a 28x28 píxeles
    img = img.resize((28, 28))

    # convertir la imagen a un array de NumPy
    img_np = np.array(img).astype('float32') / 255

    # invertir los colores: MNIST tiene números en blanco sobre fondo negro
    img_np = 1 - img_np  # invertir los valores de píxeles

    # asegurarse de que el array tiene las dimensiones correctas (28, 28, 1)
    img_np = img_np.reshape(1, 28, 28, 1)

    return img_np

def predict_and_display(images_paths, model):
    num_images = len(images_paths)
    
    # crear un grid para mostrar las imágenes
    fig, axs = plt.subplots(1, num_images, figsize=(20, 20))

    for i, img_path in enumerate(images_paths):
        # preprocesar la imagen
        img_np = preprocess_image(img_path)

        # hacer la predicción para la imagen
        prediction = model.predict(img_np)
        predicted_label = np.argmax(prediction)

        # mostrar la imagen con la predicción
        axs[i].imshow(img_np.squeeze(), cmap='gray')
        axs[i].set_title(f'Predicción: {predicted_label}')
        axs[i].axis('off')

    plt.show()

# lista de rutas de las imágenes
image_paths = ['sample_data/0.jpg', 'sample_data/1.jpg', 'sample_data/2.jpg', 'sample_data/3.jpg', 'sample_data/4.jpg', 
               'sample_data/5.jpg', 'sample_data/6.jpg', 'sample_data/7.jpg', 'sample_data/8.jpg', 'sample_data/9.jpg']

# llamar a la función para predecir y mostrar
predict_and_display(image_paths, model)