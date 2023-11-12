import firebase_admin
from flask import Flask, request, jsonify
from firebase_admin import auth, credentials, db

from werkzeug.utils import secure_filename
import os

import disease_detection

app = Flask(__name__)
cred = credentials.Certificate("secret.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://vitalisee-52dc6-default-rtdb.firebaseio.com/'
})

ALLOWED_EXTENSIONS = ['jpeg']

# TODO: change uploads folder to a proper path
app.config['UPLOAD_FOLDER'] = "./uploads"

@app.route('/')
def home():
    # Retrieve data from Firebase
    data = db.reference('data/users/john').get()
    return jsonify(data)

@app.route('/login', methods=['post'])
def login():
    username = request.form['username']
    password = request.form['password']

    # Check the username and password against Firebase
    try:
        userdata = db.reference('data/users/' + username).get()
        if userdata:
            if password == userdata["password"]:
                 return 'Login successful'
            return 'Incorrect password'
        else:
            return 'Invalid username'
    except auth.UserNotFoundError:
        return 'Invalid username'
    
@app.route('/signup', methods=['post'])
def signup():
    username = request.form['username']
    password = request.form['password']

    if not username.isalpha():
        return 'Username can only be alphabetical'

    ref = db.reference('data/users/' + username)

    if ref.get():
        return 'User already exists'
    
    ref.set({'password': password})

    return 'Created user successfully'
    

@app.route('/predict', methods=['post'])
def predict():

    if 'file' not in request.files:
        return 'File not received'
    
    file = request.files['file']

    # Ensure file extension allowed
    if (file.filename.split(".")[-1] not in ALLOWED_EXTENSIONS):
        return 'Invalid file type'
    
    filename = secure_filename(file.filename)
    filePath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filePath)

    res = disease_detection.predict(filePath)

    os.remove(filePath)

    return res
    


