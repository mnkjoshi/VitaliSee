import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf

MODEL = tf.keras.models.load_model("/content/3")
CLASS_NAMES = ['Pepper__bell___Bacterial_spot', 'Pepper__bell___healthy', 'Potato___Early_blight',
               'Potato___Late_blight', 'Potato___healthy', 'Tomato_Bacterial_spot', 'Tomato_Early_blight',
               'Tomato_Late_blight', 'Tomato_Leaf_Mold', 'Tomato_Septoria_leaf_spot',
               'Tomato_Spider_mites_Two_spotted_spider_mite', 'Tomato__Target_Spot',
               'Tomato__YellowLeaf__Curl_Virus', 'Tomato__mosaic_virus', 'Tomato_healthy']

def read_file_as_image(data) -> np.ndarray:
    image = np.array(Image.open(BytesIO(data)))
    return image

def predict(file_path):
    with open(file_path, "rb") as f:
        image = read_file_as_image(f.read())

    img_batch = np.expand_dims(image, 0)
    prediction = MODEL.predict(img_batch)
    predicted_class = CLASS_NAMES[np.argmax(prediction[0])]
    confidence = np.max(prediction[0])

    return {'class': predicted_class, 'confidence': float(confidence)}

if __name__ == "__main__":
    image_file_path = "/content/potato_exl.jpeg"  # Replace with the path to your image file
    result = predict(image_file_path)
    print(result)
