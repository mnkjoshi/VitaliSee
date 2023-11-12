import tensorflow as tf
from PIL import Image
import numpy as np

model = None
class_names = ["Early Blight", "Late Blight", "Healthy"]

def load_model():
    global model
    if model is None:
        model = tf.keras.models.load_model("/content/potato_Detection.h5")  # Replace with your actual model path

def preprocess_image(image_path):
    image = np.array(
        Image.open(image_path).convert("RGB").resize((256, 256))
    )
    image = image / 255.0  # Normalize to [0, 1]
    return image

def predict(image_path):
    load_model()
    image = preprocess_image(image_path)
    img_array = tf.expand_dims(image, 0)
    predictions = model.predict(img_array)
    predicted_class = class_names[np.argmax(predictions[0])]
    confidence = round(np.max(predictions[0]), 2)
    return {"class": predicted_class, "confidence": confidence}

result = predict('/content/potato_exe.jpeg')
print(result)
