import cv2
import joblib
import numpy as np


# Define the path to your pre-trained model
model_path = "D:\SkinSightAdditional\skin_disease_svm_improve_final.pkl"  # Update with the correct path

# Load the pre-trained model
model = joblib.load(model_path)

# Define a list of class labels
class_labels = ['Atopic Dermatitis', 'Basal Cell Carcinoma', 'Melanoma', 'Echzema', 'Melanocytic Nevi']

def preprocess_and_predict(image_file):
    # Read the image file from the file object
    image = cv2.imdecode(np.fromstring(image_file.read(), np.uint8), cv2.IMREAD_COLOR)
    image = cv2.resize(image, (224, 224))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = image.flatten()  # Flatten the image into a 1D array

    # Make a prediction using the loaded model
    prediction = model.predict(np.array([image]))
    #predicted_index = np.argmax(prediction)

# Get the corresponding class label
    predicted_class = prediction

    # Access the predicted class label


    return predicted_class
