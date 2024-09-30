import numpy as np
import os
import cv2

rows = 122
cols = 360
channels = 1
window = 5
categories = [0, 35, 70, 119, 177, 220, 255]
horizon = 4

# Set the path to the folder containing the images
path = "ConvLSTM\DroughtDatasetMask"

# Get a list of all the image file names in the folder
image_files = [f for f in os.listdir(path) if f.endswith('.jpg') or f.endswith('.png')]

# Suponiendo que todas las imágenes tienen el tamaño deseado de 122x360
num_images = len(image_files)  # Asegúrate de que este número corresponde al número de imágenes que deseas cargar

# Verifica que tengas la cantidad correcta de archivos de imagen
if len(image_files) != num_images:
    raise ValueError(f"Expected {num_images} images, but found {len(image_files)}")

# Create an empty numpy array to hold the images
images = np.zeros((num_images, rows, cols), dtype=np.uint8)  # Asegúrate de que el tipo de datos sea correcto

# Loop through the image files and add each image to the numpy array
for i, file in enumerate(sorted(image_files)[:num_images]):  # Asegúrate de que no excedas el número de imágenes deseado
    # Load the image using OpenCV
    img = cv2.imread(os.path.join(path, file), cv2.IMREAD_GRAYSCALE)  # Directamente en escala de grises
    if img.shape != (rows, cols):
        raise ValueError(f"The image {file} has a shape of {img.shape}, but expected {(rows, cols)}")
    # Add the image to the numpy array
    images[i] = img

# Save the numpy array to a file
np.save("ConvLSTM\Models\DroughtDatasetMask.npy", images)
print("Images shape: {}".format(images.shape))