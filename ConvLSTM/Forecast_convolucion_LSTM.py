import pandas as pd
from pandas import DataFrame
from keras.preprocessing import image
import numpy as np
import matplotlib.pyplot as plt
import cv2
from keras.callbacks import TensorBoard, Callback
import tensorflow as tf
from tensorflow import keras
from mpl_toolkits.mplot3d import axes3d
from keras import backend as K
import gc
import time
from app.common.color_tools import *
from app.data_treatment.load_imgs import *
import multiprocessing
from concurrent.futures import ProcessPoolExecutor
from tqdm import tqdm
from tensorflow.keras.layers import Conv2D, Lambda
from random import random

class CustomCallback(Callback):
    def __init__(self, model, x_test):
        self.model = model
        self.x_test = x_test
    
    def on_epoch_end(self, epoch, logs={}):
        y_pred = self.model.predict(self.x_test[:1], batch_size= 2)
        plt.figure(figsize=(10,10))
        plt.imshow(y_pred[0], cmap='gray')
        plt.show()

# Función que carga y prepara los datos
def load_and_prepare_all_data(rows= 122, cols= 360, channels= 1):
    x = load_imgs("/kaggle/working/DroughtDatasetMask", "/kaggle/working/DroughtDatasetMask/NamesDroughtDataset.csv", rows, cols)
    x = x.astype('float32')
    x = x.reshape(len(x), rows, cols, channels)
    print('Data shape: {}'.format(x.shape))
    return x

# Sirve para generar los cubos de información x, además asignar el objetivo y
def create_shifted_frames(data):
    x = data[:, 0 : data.shape[1] - 1, :, :]
    y = data[:, 1 : data.shape[1], :, :]
    return x, y

# Sirve para generar los cubos de información x, además asigna el objetivo y
def create_shifted_frames_2(data):
    x = data[:, 0 : data.shape[1] - 1, :, :]
    y = data[:, data.shape[1]-1, :, :]
    return x, y

def agroup_window(data, window):
    new_data = [data[i:window+i] for i in range(len(data)-window+1)]
    return np.array(new_data)

def to_monochromatic(img_data, min_val= 10, max_val= 255):
    x_mono = []
    for i in img_data:
        (thresh, monoImg) = cv2.threshold(i, min_val, max_val, cv2.THRESH_BINARY)
        x_mono.append(monoImg)
    x_mono = np.array(x_mono)
    return x_mono

def add_last(data, new_vals):
    print(data.shape)
    x_test_new = data[:,1:]
    print(x_test_new.shape)
    print(new_vals.shape)
    l = []
    for i in range(len(x_test_new)):
        l.append(np.append(x_test_new[i], new_vals[i]))
    x_test_new = np.array(l).reshape(data.shape[:])
    print("CX", x_test_new.shape)
    return x_test_new

def recolor(args):
    data, pallete = args
    res = gray_quantized(data, pallete)
    res = recolor_greys_image(res, pallete)
    return np.array(res)

def limit_memory():
    """ Release unused memory resources. Force garbage collection """
    K.clear_session()
    gc.collect()

def binary_to_decimal(binary_number):
    """
    Convierte un número binario (lista de 0 y 1) a su valor decimal.
    """
    number = 0
    for b in binary_number:
        number = (2 * number) + int(b)
    return number

def cromosome_to_params(cromosome):
    print(len(cromosome))
    """
    Decodifica un cromosoma en una configuración de hiperparámetros para un modelo de aprendizaje profundo.

    Parámetros:
        cromosome (list[int]): Lista binaria que representa los hiperparámetros codificados.

    Retorna:
        dict: Configuración de hiperparámetros.
    """
    # Constantes
    KERNEL_SIZE = [(1, 1), (3, 3), (5, 5), (7, 7)]
    FILTERS_OPTIONS = [8, 16, 24, 32, 40, 48, 56, 64]
    LEARNING_RATE_OPTIONS = [
        0.0001, 0.000215, 0.000464, 0.001, 0.00215, 
        0.00464, 0.01, 0.0215, 0.0464, 0.1
    ]
    REDUCTION_RATE_OPTIONS = [0.1, 0.2, 0.3, 0.4, 0.5]
    WINDOW_SIZE_OPTIONS = list(range(1, 11))  # Tamaño ventana de entrada (1-10)
    BATCH_SIZE_OPTIONS = [1, 8, 16, 24, 32, 40, 48, 56, 64]
    PATIENCE_OPTIONS = list(range(2, 11))  # 2 a 10
    LOSS_FUNCTIONS = ["binary_crossentropy", "kullback_leibler_divergence"]
    OPTIMIZERS = ["SGD", "Adam", "RMSprop", "Adagrad", "Adadelta", "Nadam", "Ftrl"]

    # Índice dinámico
    idx = 0

    # Número de capas ConvLSTM
    num_conv_layers = binary_to_decimal(cromosome[idx:idx + 3]) + 1  # Rango 1-6
    idx += 3

    # Configuración de capas ConvLSTM
    conv_layers = []
    for i in range(num_conv_layers):
        # Número de filtros (3 bits)
        filters = FILTERS_OPTIONS[binary_to_decimal(cromosome[idx:idx + 3])]
        idx += 3

        # Tamaño del kernel (2 bits)
        kernel_size = KERNEL_SIZE[binary_to_decimal(cromosome[idx:idx + 2])]
        idx += 2

        # Capa de normalización (1 bit)
        normalization = bool(binary_to_decimal(cromosome[idx:idx + 1]))
        idx += 1

        conv_layers.append({
            "filters": filters,
            "kernel_size": kernel_size,
            "normalization": normalization
        })

    # Tamaño del kernel capa Conv2D
    kernel_conv2d = KERNEL_SIZE[binary_to_decimal(cromosome[idx:idx + 2])]
    idx += 2

    # Tamaño de la ventana de entrada
    window_size = WINDOW_SIZE_OPTIONS[binary_to_decimal(cromosome[idx:idx + 4])]
    idx += 4

    # Batch size
    batch_size = BATCH_SIZE_OPTIONS[binary_to_decimal(cromosome[idx:idx + 4])]
    idx += 4

    # Learning rate
    learning_rate = LEARNING_RATE_OPTIONS[binary_to_decimal(cromosome[idx:idx + 4])]
    idx += 4

    # Tasa de reducción de aprendizaje
    reduction_rate = REDUCTION_RATE_OPTIONS[binary_to_decimal(cromosome[idx:idx + 3])]
    idx += 3

    # Paciencia para reducción de aprendizaje
    patience_reduction = PATIENCE_OPTIONS[binary_to_decimal(cromosome[idx:idx + 4])]
    idx += 4

    # Paciencia para EarlyStopping
    patience_early_stopping = PATIENCE_OPTIONS[binary_to_decimal(cromosome[idx:idx + 4])]
    idx += 4

    # Función de pérdida (1 bit)
    loss_function = LOSS_FUNCTIONS[binary_to_decimal(cromosome[idx:idx + 1])]
    idx += 1

    # Optimizador
    optimizer = OPTIMIZERS[binary_to_decimal(cromosome[idx:idx + 3])]
    idx += 3

    # Configuración final
    model_config = {
        "num_conv_layers": num_conv_layers,
        "conv_layers": conv_layers,
        "kernel_conv2d": kernel_conv2d,
        "window_size": window_size,
        "batch_size": batch_size,
        "learning_rate": learning_rate,
        "reduction_rate": reduction_rate,
        "patience_reduction": patience_reduction,
        "patience_early_stopping": patience_early_stopping,
        "loss_function": loss_function,
        "optimizer": optimizer,
    }

    return model_config

def fitness_function(cromosome):
    # Decodifica los hiperparámetros del cromosoma
    params = cromosome_to_params(cromosome)
    
    # Parámetros iniciales
    window = params["window_size"]
    channels = 1
    rows = 122
    cols = 360
    categorical = False
    categories = np.array([0, 35, 70, 119, 177, 220, 255]) #[0,51,102,153,204,255]
    # Manejar este valor en 1, para generar solo la siguiente imagen
    horizon = 1
    name = 'Model_autoML_testing_{}'.format(int(time.time()))

    # Imágenes en color, no es necesario utilizarla
    if categorical:
        x = np.load("Models/Data_full_select_color.npy") * 255
        x = x.astype(np.uint8)
        # Obtención de la paleta de colores, se toma una imagen muestra
        aux = x[1168]
        res = n_colors_img(aux, 6)
        colors = get_colors(res).reshape(6,1,3)
        print(len(colors))
        # Se utiliza una función de cuantificación en las imágenes para que
        # todas las imágenes manejen una paleta de colores.
        aux_data = np.array([rgb_quantized(i, colors) for i in x])
        print(aux_data.shape)
        # Se comprueban los colores obtenidos
        c1 = get_colors(aux_data[0])
        c2 = get_colors(aux_data[1167])
        print(c1)
        print(c2)
        # Se transforma el dataset de colores a escala de grieses, cv2 para mejor calidad.
        x_greys = np.array([cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) for img in aux_data])
        #np.save('Models/Data_full_select_greys.npy', x_greys)
        colors_greys = get_colors(x_greys[1168])
        cg1 = get_colors(x_greys[0])
        cg2 = get_colors(x_greys[1167])
        print(cg1)
        print(cg2)
        a1 = x_greys[0]
        a2 = x_greys[1167]
        x_greys = np.array([balance_img_categories(img, colors_greys, categories) for img in x_greys])
        ig1 = x_greys[0]
        ig2 = x_greys[1167]
        print(get_colors(ig1))
        print(get_colors(ig2))
        x = x_greys.astype('float32') / 255
    else:
        x = load_and_prepare_all_data().astype(np.uint8)
        #Cargar imágenes en memoria, y almacenar en una estructura numpy
        #x = np.load("Models/DroughtDatasetMask.npy").astype(np.uint8)
        #x = np.load('Models/SPIDatasetMask.npy').astype(np.uint8) #/255
        print(get_colors(x[-1]))
        print(x[-1].max())
        #Mostrar imágenes
        fig, axes = plt.subplots(2, 3, figsize= (10,8))

        data_choise = np.random.choice(range(len(x)), size= 1)[0]
        for idx, ax in enumerate(axes.flat):
            ax.imshow(np.squeeze(x[data_choise+idx]), cmap='gray')
            ax.set_title(f"Frame {idx + 1}")
            ax.axis("off")

        #print("Displaying frames for example {}".format(data_choise))
        plt.show()
        
        args = [(d, categories) for d in x]

        num_cores = max(1, multiprocessing.cpu_count() - 4)
        with ProcessPoolExecutor(max_workers=num_cores) as pool:
            with tqdm(total = len(x)) as progress:
                futures = []

                for img in args:
                    future = pool.submit(recolor, img)
                    future.add_done_callback(lambda p: progress.update())
                    futures.append(future)
                
                results = []
                for future in futures:
                    result = future.result()
                    results.append(result)
        x_greys = np.array(results)
        #x = np.array([gray_quantized(i, np.array(categories)) for i in x])
        colors_greys = get_colors(x_greys[-1])
        print(colors_greys)
        #x_greys = np.array([recolor_greys_image(img, categories) for img in x])
        x = x_greys.astype('float32') / 255
        print(get_colors(x[-1]))
    #x = np.load("Models/Data_full_select_greys.npy")
    print(x.shape)

    #Mostrar imágenes
    fig, axes = plt.subplots(2, 3, figsize= (10,8))

    data_choise = np.random.choice(range(len(x)), size= 1)[0]
    for idx, ax in enumerate(axes.flat):
        ax.imshow(np.squeeze(x[data_choise+idx]), cmap='gray')
        ax.set_title(f"Frame {idx + 1}")
        ax.axis("off")

    #print("Displaying frames for example {}".format(data_choise))
    plt.show()

    x_2 = agroup_window(x, window)
    print(x_2.shape)
    x_train = x_2[:int(len(x_2)*.7)]
    x_test = x_2[int(len(x_2)*.7):]
    x_validation = x_train[int(len(x_train)*.8):]
    x_train = x_train[:int(len(x_train)*.8)]

    #x_trian = x_train.astype('float32') / 255
    #x_validation = x_validation.astype('float32') / 255
    #x_test = x_test.astype('float32') / 255
    x_train = x_train.reshape(len(x_train), window, rows, cols, channels)
    x_validation = x_validation.reshape(len(x_validation), window, rows, cols, channels)
    x_test = x_test.reshape(len(x_test), window, rows, cols, channels)
    
    print("Forma de datos de entrenamiento: {}".format(x_train.shape))
    print("Forma de datos de validación: {}".format(x_validation.shape))
    print("Forma de datos de pruebas: {}".format(x_test.shape))

    x_train, y_train = create_shifted_frames_2(x_train)
    x_validation, y_validation = create_shifted_frames_2(x_validation)
    x_test, y_test = create_shifted_frames_2(x_test)

    print("Training dataset shapes: {}, {}".format(x_train.shape, y_train.shape))
    print("Validation dataset shapes: {}, {}".format(x_validation.shape, y_validation.shape))
    print("Test dataset shapes: {}, {}".format(x_test.shape, y_test.shape))

    np.save("/kaggle/working/Models/x_test_convlstm_greys_forecast.npy", x_test)
    np.save("/kaggle/working/Models/y_test_convlstm_greys_forecast.npy", y_test)
    
    #Mostrar imágenes
    #fig, axes = plt.subplots(2, 3, figsize= (10,8))

    #data_choise = np.random.choice(range(len(x_2)), size= 1)[0]
    #for idx, ax in enumerate(axes.flat):
    #    ax.imshow(np.squeeze(x_2[data_choise][idx]), cmap='gray')
    #    ax.set_title(f"Frame {idx + 1}")
    #    ax.axis("off")

    #print("Displaying frames for example {}".format(data_choise))
    #plt.show()

    #strategy = tf.distribute.MirroredStrategy()
    strategy = tf.distribute.OneDeviceStrategy(device='/GPU:0')
    with strategy.scope():
        
        # Construcción del modelo dinámico basado en los parámetros decodificados
        inp = keras.layers.Input(shape=(None, rows, cols, channels))
        m = inp

        for layer in params["conv_layers"]:
            m = keras.layers.ConvLSTM2D(
                filters=layer["filters"],
                kernel_size=layer["kernel_size"],
                padding="same",
                return_sequences=True,
                activation="relu"
            )(m)
            if layer["normalization"]:
                m = keras.layers.BatchNormalization()(m)
        
        # Reducción del eje temporal
        m = Lambda(lambda x: x[:, -1])(m)
        
        # Aplicar Conv2D a cada paso temporal
        m = Conv2D(channels, kernel_size=params["kernel_conv2d"], activation="sigmoid", padding="same")(m)

        model = keras.models.Model(inp, m)
        
        optimizer_name = params["optimizer"]
        optimizer_class = getattr(tf.keras.optimizers, optimizer_name)
        optimizer = optimizer_class(params["learning_rate"])
        
        model.compile(loss=params["loss_function"], optimizer=optimizer)

        print(model.summary())

        #Callbacks
        early_stopping = keras.callbacks.EarlyStopping(monitor= "val_loss", patience=params["patience_early_stopping"], restore_best_weights= True)
        reduce_lr = keras.callbacks.ReduceLROnPlateau(monitor= "val_loss", patience=params["patience_reduction"])

        board = TensorBoard(log_dir='logs/{}'.format(name))

        #Define moifiable training hyperparameters
        epochs = 10
        batch_size = params["batch_size"]

        #Model training
        model.fit(
            x_train, y_train,
            batch_size = batch_size,
            epochs = epochs,
            validation_data= (x_validation, y_validation),
            #callbacks= [early_stopping, reduce_lr, board, CustomCallback(model, x_test)]
            callbacks= [reduce_lr, early_stopping]
        )

        example = x_test[np.random.choice(range(len(x_test)), size= 1)[0]]

        #frames = example[:4, ...]
        #original_frames = example[4:, ...]
        print(example.shape)
        #print(frames.shape)
        #print(original_frames.shape)

        for _ in range(horizon):
            print(example.shape)
            new_prediction = model.predict(example.reshape(1,*example.shape[0:]))
            example = np.concatenate((example[1:], new_prediction), axis=0)
            print(example.shape)

        predictions = example[:-4]
        print(predictions.shape)
        #fig, axes = plt.subplots(2,4, figsize= (20,4))
        #for idx, ax in enumerate(axes[0]):
        #    ax.imshow((predictions[idx]), cmap='gray')
        #    ax.set_title("Frame {}".format(idx+3))
        #    ax.axis("off")
        #plt.show()
        err = model.evaluate(x_test, y_test, batch_size= 2)
        print("El error del modelo es: {}".format(err))
        preds = model.predict(x_test, batch_size= 2)
        print(preds.shape)
        
        #Esto es para pronósticar a un horizonte más largo
        x_test_new = add_last(x_test, preds[:])
        preds2 = model.predict(x_test_new, batch_size= 2)
        #print(preds2.shape)
        x_test_new = add_last(x_test_new, preds2[:])
        preds3 = model.predict(x_test_new, batch_size= 2)
        x_test_new = add_last(x_test_new, preds3[:])
        preds4 = model.predict(x_test_new, batch_size= 2)
        res_forecast = add_last(x_test_new, preds4[:])
        print("PREDSS",res_forecast.shape)


        if categorical:
            np.save("/kaggle/working/Models/PredictionsConvolutionLSTM_greys_forecast_1.npy", res_forecast)
        else:
            np.save("/kaggle/working/Models/PredictionsConvolutionLSTM_forecast_1.npy", res_forecast)
            
        # Evaluamos el rendimiento del modelo en el conjunto de validación
        val_accuracy = model.evaluate(x_validation, y_validation, verbose=0)
        print("Precisión en el conjunto de validación: {:.2f}".format(val_accuracy))
        
        # Devolvemos la precisión en el conjunto de validación
        return val_accuracy

class Solution(object):
    def __init__(self, value):
        self.value = value
        self.fitness = None

    def calculate_fitness(self, fitness_function):
        self.fitness = fitness_function(self.value)

def generate_candidate(vector):
    value = ""
    for p in vector:
        value += "1" if random() < p else "0"
    return Solution(value)

def generate_vector(size):
    return [0.5] * size  # Empieza con probabilidades del 50%

def compete(a, b):
    if a.fitness > b.fitness:
        return a, b
    else:
        return b, a

def update_vector(vector, winner, loser, population_size):
    for i in range(len(vector)):
        if winner[i] != loser[i]:
            if winner[i] == '1':
                vector[i] += 1.0 / float(population_size)
            else:
                vector[i] -= 1.0 / float(population_size)

def run(generations, size, population_size, fitness_function):
    vector = generate_vector(size)
    best = None
    
    for i in range(generations):
        s1 = generate_candidate(vector)
        s2 = generate_candidate(vector)

        s1.calculate_fitness(fitness_function)
        s2.calculate_fitness(fitness_function)

        winner, loser = compete(s1, s2)

        if best:
            if winner.fitness > best.fitness:
                best = winner
        else:
            best = winner 
        
        update_vector(vector, winner.value, loser.value, population_size)

        print(f"Generation: {i + 1}, Best value: {best.value}, Best fitness: {float(best.fitness)}")
        
    return best.value  # Devolvemos el mejor cromosoma encontrado

if __name__ == '__main__':
    
    # Generamos un cromosoma de tamaño 44
    cromosoma_optimo = run(1000, 44, 10, fitness_function)
    print("Cromosoma óptimo encontrado:", cromosoma_optimo)