from flask import Flask, request, jsonify
from firebase_admin import auth

from werkzeug.utils import secure_filename
import os


app = Flask(__name__)

# TODO: change uploads folder to a proper path
app.config['UPLOAD_FOLDER'] = "uploads"

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
    
@app.route('/signup', methods=['post'])
def signup():
    username = request.form['username']
    password = request.form['password']

    try:
        user = auth.create_user(
            email=username,
            password=password
        )
    except auth.EmailAlreadyExistsError:
        return 'Email already in use'
    
    return 'Create user successful'

@app.route('/predict', methods=['post'])
def predict():
    allowedExtensions = ['jpeg']

    if 'file' not in request.files:
        return 'File not received'
    
    file = request.files['file']

    # Ensure file extension allowed
    if (file.filename.split(".")[-1] not in allowedExtensions):
        return 'Invalid file type'
    
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    return 'Upload image successful'
    


