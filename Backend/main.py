import firebase_admin
from flask import Flask, request, jsonify
from firebase_admin import auth, credentials, db

from werkzeug.utils import secure_filename
import os

import base64
import json
import re

import disease_detection
import extension

app = Flask(__name__)
cred = credentials.Certificate("secret.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://vitalisee-52dc6-default-rtdb.firebaseio.com/'
})

ALLOWED_EXTENSIONS = ['jpeg']
DATE_PATTERN = re.compile(r'^\d{2}-\d{2}-\d{4}$')

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
            if password == userdata["password"]: # type: ignore
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
    locationToSet = request.form['location']
    # Ensure file extension allowed
    if (not file.filename or file.filename.split(".")[-1] not in ALLOWED_EXTENSIONS):
        return 'Invalid file type'
    
    filename = secure_filename(file.filename)
    filePath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filePath)

    res = disease_detection.predict(filePath)

    os.remove(filePath)
    if res['class'] not in ['Potato___healthy', 'Tomato_healthy', 'Pepper__bell___healthy'] and locationToSet:
        diseaseData = db.reference('data/locations/').get()
        disRef = db.reference('data/locations/' + len(diseaseData))
        disRef.set(locationToSet)
    return res['class']

@app.route('/<username>/save-growth', methods=['post'])
def saveGrowth(username):
    
                             
    if 'file' not in request.files:
        return 'File not received'
    
    picture = request.files['file']
    date = request.form['date']

    if not DATE_PATTERN.match(date):
        return 'Date does not follow "DD-MM-YYYY"'
    
    if db.reference(f'data/uTrackers/{username}/growth/{date}').get():
        return 'Photo on date already exists'

    refGrowthPic = db.reference(f'data/uTrackers/{username}/growth')

    # Ensure file extension allowed
    if (not picture.filename or picture.filename.split(".")[-1] not in ALLOWED_EXTENSIONS):
        return 'Invalid file type'
    
    pictureName = secure_filename(picture.filename)
    path = os.path.join(app.config['UPLOAD_FOLDER'], pictureName)
    picture.save(path)

    with open(path, "rb") as pictureFile:
        encodedStr = base64.b64encode(pictureFile.read()).decode('utf-8')

        refGrowthPic.set({date: json.dumps(str(encodedStr))})


    os.remove(path)

    return 'Saved succesfully'


@app.route('/<username>/<date>', methods=['get'])
def getGrowth(username, date):
    if not DATE_PATTERN.match(date):
        return 'Date does not follow "DD-MM-YYYY"'
    
    jsonPhoto = db.reference(f'data/uTrackers/{username}/growth/{date}').get()

    if not jsonPhoto:
        return 'Date does not exist'
    
    # Save photo in folder
    with open('uploads/img.jpeg', 'wb') as photo:
        photoBytes = base64.b64decode(json.loads((str(jsonPhoto))))
        photo.write(photoBytes)
  
    return photoBytes