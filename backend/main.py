from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf
from firebase_admin import auth, exceptions

app = Flask(__name__)
CORS(app)
MODEL = tf.keras.models.load_model("../saved_models/3")
CLASS_NAMES = ['Pepper__bell___Bacterial_spot', 'Pepper__bell___healthy', 'Potato___Early_blight',
               'Potato___Late_blight', 'Potato___healthy', 'Tomato_Bacterial_spot', 'Tomato_Early_blight',
               'Tomato_Late_blight', 'Tomato_Leaf_Mold', 'Tomato_Septoria_leaf_spot',
               'Tomato_Spider_mites_Two_spotted_spider_mite', 'Tomato__Target_Spot',
               'Tomato__YellowLeaf__Curl_Virus', 'Tomato__mosaic_virus', 'Tomato_healthy']

@app.route('/login', methods=['post'])
def login():
    username = request.form['username']
    password = request.form['password']

    # Check the username and password against Firebase
    try:
        user = auth.get_user_by_email(username)
        if auth.verify_id_token(user.uid, password):
            return 'Login successful'
        else:
            return 'Invalid password'
    except auth.UserNotFoundError:
        return 'Invalid username'
    
@app.route('signup', methods=['post'])
def signup():
    username = request.form['username']
    password = request.form['password']

    user = auth.create_user(
        username=username,
        password=password
    )
@app.route('/ping', methods=['GET'])
def ping():
    return "Hello I'm alive"

def read_file_as_image(data):
    image = np.array(Image.open(BytesIO(data)))
    return image

@app.route('/predict', methods=['POST'])
def predict():
    file = request.files.get('file')
    if not file:
        return jsonify({'error': 'No file provided'}), 400

    image = read_file_as_image(file.read())
    img_batch = np.expand_dims(image, 0)
    prediction = MODEL.predict(img_batch)
    
    predicted_class = CLASS_NAMES[np.argmax(prediction[0])]
    confidence = float(np.max(prediction[0]))

    return jsonify({
        'class': predicted_class,
        'confidence': confidence
    })
