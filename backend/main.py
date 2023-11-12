from flask import Flask, request, jsonify
from firebase_admin import auth, exceptions

app = Flask(__name__)

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

