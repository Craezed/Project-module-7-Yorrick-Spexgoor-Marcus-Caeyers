import cv2
import keras.models
import numpy
import numpy as np
from PIL import Image
import os

from sklearn.metrics import confusion_matrix
from keras.src.metrics.accuracy_metrics import accuracy
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
import tensorflow as tf
from sklearn.model_selection import GridSearchCV
from scikeras.wrappers import KerasClassifier
from sklearn.metrics import ConfusionMatrixDisplay
import matplotlib.pyplot as plt

IMG_SIZE = [128, 128]

def TrainAI():
    X = []
    y = []

    X = np.array(X)
    y = np.array(y)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    X_train, X_test = X_train / 255.0, X_test / 255.0

    def create_model():
        model = tf.keras.models.Sequential([
            tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(IMG_SIZE[0], IMG_SIZE[1], 4)),
            tf.keras.layers.MaxPooling2D((2, 2)),
            tf.keras.layers.Conv2D(16, (3, 3), activation='relu'),
            tf.keras.layers.MaxPooling2D((2, 2)),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(32, activation='relu'),
            tf.keras.layers.Dense(2, activation='softmax')
        ])
        model.compile(optimizer='adam', loss="sparse_categorical_crossentropy", metrics=["accuracy"])
        return model

    ## GridSearch ##
    #Create Keras model for GridSearch
    keras_model = KerasClassifier(model=create_model())

    parameters = {
        'batch_size': [32],
        'epochs': [12],
        'optimizer': ['adam'],
       'validation_split': [0.1]
    }

    grid = GridSearchCV(estimator=keras_model, param_grid=parameters, cv=3, n_jobs=1)
    grid_result = grid.fit(X_train, y_train)

    print(f"Best Parameters: {grid_result.best_params_}")
    print(f"Best Score: {grid_result.best_score_}")

    ## Train Model ##
    # model = create_model()
    # model.fit(X_train, y_train, batch_size=32, epochs=12, validation_split=0.1)
    # test_loss, test_acc = model.evaluate(X_test, y_test)
    # print(test_loss)
    # print(test_acc)
    #
    # matrix = confusion_matrix(np.argmax(model.predict(X_test), 1), y_test)
    #
    # disp = ConfusionMatrixDisplay(matrix)
    # disp.plot()
    # plt.show()
    #
    # model.save("model.keras")

