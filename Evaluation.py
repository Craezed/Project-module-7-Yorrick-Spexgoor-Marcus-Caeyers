from keras.models import load_model
import matplotlib.pyplot as plt

model = load_model("model.keras")


# Plot confusion matrix
matrix = confusion_matrix(np.argmax(model.predict(X_test), 1), y_test)
disp = ConfusionMatrixDisplay(matrix)
disp.plot()
plt.show()