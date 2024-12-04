def binary_to_decimal(binary_number):
    """
    Convierte un número binario (lista de 0 y 1) a su valor decimal.
    """
    number = 0
    for b in binary_number:
        number = (2 * number) + b
    return number

def cromosome_to_params(cromosome):
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

