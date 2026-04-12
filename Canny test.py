import numpy as np
from PIL import Image
import os
import matplotlib.pyplot as plt
import pygame

from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.model_selection import train_test_split
import tensorflow as tf
from sklearn.model_selection import GridSearchCV
from scikeras.wrappers import KerasClassifier
import cv2
IMG_SIZE = [320, 320]
label_key = ['a', 'c', 'e', 'i', 'l', 'n', 'o', 'r', 's', 't']

def DataPrep():
    X = []
    y = []
    for folder in os.listdir("data"):
        for file in os.listdir(f"data/{folder}"):
            if file.lower().endswith(".png"):
                img = cv2.imread(f"data/{folder}/{file}")
                img = cv2.Canny(img, 100, 200)
                img_array = img.astype(np.float32) / 255.0
                X.append(img_array)
                y.append(label_key.index(folder))

    return X, y

def create_model():
    model = tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu', padding='same', input_shape=(IMG_SIZE[0], IMG_SIZE[1], 1)),
        tf.keras.layers.MaxPooling2D(2, 2),

        tf.keras.layers.Conv2D(48, (3, 3), activation='relu', padding='same'),
        tf.keras.layers.MaxPooling2D(2, 2),

        tf.keras.layers.Conv2D(56, (3, 3), activation='relu', padding='same'),
        tf.keras.layers.MaxPooling2D(2, 2),

        tf.keras.layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
        tf.keras.layers.MaxPooling2D(2, 2),

        tf.keras.layers.Conv2D(72, (3, 3), activation='relu', padding='same'),
        tf.keras.layers.MaxPooling2D(2, 2),

        tf.keras.layers.Conv2D(80, (3, 3), activation='relu', padding='same'),
        tf.keras.layers.MaxPooling2D(2, 2),

        tf.keras.layers.Conv2D(96, (3, 3), activation='relu', padding='same'),
        tf.keras.layers.Flatten(),

        tf.keras.layers.Dense(100, activation='relu'),
        tf.keras.layers.Dense(10, activation='softmax')
    ])
    model.compile(optimizer='adam', loss="sparse_categorical_crossentropy", metrics=["accuracy"])
    return model

def gridsearch_train():
    X, y = DataPrep()
    X = np.array(X)
    y = np.array(y)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    ## GridSearch ##
    # Create Keras model for GridSearch
    keras_model = KerasClassifier(model=create_model())

    parameters = {
        'batch_size': [24, 32, 48],
        'epochs': [20, 25],
        'optimizer': ['adam', 'sgd'],
        'validation_split': [0.1, 0.2]
    }

    grid = GridSearchCV(estimator=keras_model, param_grid=parameters, cv=3, n_jobs=1, refit=True)
    grid_result = grid.fit(X_train, y_train)
    classifier = grid.best_estimator_
    classifier.model.save("GCVModel.keras")

    print(f"Best Parameters: {grid_result.best_params_}")
    print(f"Best Score: {grid_result.best_score_}")


def regular_train():
    ## Train Model ##
    X, y = DataPrep()
    X = np.array(X)
    y = np.array(y)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = create_model()
    history = model.fit(X_train, y_train, batch_size=32, epochs=25, validation_split=0.1)
    test_loss, test_acc = model.evaluate(X_test, y_test)
    print(test_loss)
    print(test_acc)

    # Plot loss function
    plt.figure(figsize=(5, 5))
    plt.plot(history.history['loss'], label='Train Loss', color='orange')
    plt.plot(history.history['val_loss'], label='Validation Loss', color='blue')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()
    plt.title('Training and Validation Loss')
    plt.show()

    # Plot confusion matrix
    matrix = confusion_matrix(np.argmax(model.predict(X_test), 1), y_test)
    disp = ConfusionMatrixDisplay(matrix)
    disp.plot()
    plt.show()

    model.save("model2.keras")

regular_train()

