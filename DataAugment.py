import os
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np
from PIL import Image

# Configure the ImageDataGenerator for augmentation
datagen = ImageDataGenerator(
    rotation_range=30,  # Random rotation between 0-30 degrees
    width_shift_range=0.2,  # Horizontal shift
    height_shift_range=0.2,  # Vertical shift
    zoom_range=0.2,  # Zoom in/out
    horizontal_flip=True,  # Flip horizontally
    brightness_range=[0.5, 1.5]
)

# Make 5 Augmented versions of each image
for folder in os.listdir("data"):
    for img in os.listdir(f"data/{folder}"):
        img = Image.open(f"data/{folder}/{img}")

        img_array = np.array(img)
        i = 0
        img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
        for batch in datagen.flow(img_array, batch_size=1, save_to_dir=f"data/{folder}", save_prefix="aug", save_format="png"):
            i += 1
            if i >= 5:
                break