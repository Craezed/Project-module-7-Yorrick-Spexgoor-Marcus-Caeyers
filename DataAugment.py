import os

from keras.src.legacy.preprocessing.image import flip_axis
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np
from PIL import Image

# Configure the ImageDataGenerator for augmentation
datagen = ImageDataGenerator(
    rotation_range=30,  # Random rotation between 0-30 degrees
    width_shift_range=0.1,  # Horizontal shift
    height_shift_range=0.1,  # Vertical shift
    zoom_range=0.2,  # Zoom in/out
    brightness_range=[0.5, 1.5],
    horizontal_flip=True
)

# Make 5 Augmented versions of each image
for folder in os.listdir("data"):
    for img in os.listdir(f"data/{folder}"):
        if not img.lower().startswith("aug"): # Only adapt original pictures
            img = Image.open(f"data/{folder}/{img}")

            img_array = np.array(img)
            i = 0
            img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
            for batch in datagen.flow(img_array, batch_size=1, save_to_dir=f"data/{folder}", save_prefix="aug", save_format="png"):
                i += 1
                if i >= 5:
                    break