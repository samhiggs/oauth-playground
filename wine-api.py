import yaml, os
import flask
from datetime import timedelta
from flask import Flask, jsonify, abort, redirect, url_for, session
import requests_oauthlib
from db import fetch_reviews, fetch_review, fetch_user_reviews, NotFoundError, NotAuthorizedError

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.permanent_session_data = timedelta(minutes=60)

config = yaml.safe_load(open('configuration.yml', 'r'))
CLIENT_ID = config['simplelogin']['CLIENT_ID']
CLIENT_SECRET = config['simplelogin']['CLIENT_SECRET']

AUTHORIZATION_BASE_URL = 'https://app.simplelogin.io/oauth2/authorize'
TOKEN_URL = 'https://app.simplelogin.io/oauth2/token'
USERINFO_URL = 'https://app.simplelogin.io/oauth2/userinfo'

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

@app.route('/')
def index():
    return '''
    <a href="/login">Login</a>
    '''

@app.route('/login')
def login():
    if 'email' in session:
        return redirect_url(url_for('/reviews'))
    simplelogin = requests_oauthlib.OAuth2Session(
        CLIENT_ID,
        redirect_uri='http://localhost:5000/callback'
    )
    authorization_url, state = simplelogin.authorization_url(AUTHORIZATION_BASE_URL)
    return flask.redirect(authorization_url)

@app.route('/callback')
def callback():
    simplelogin = requests_oauthlib.OAuth2Session(CLIENT_ID)
    simplelogin.fetch_token(
        TOKEN_URL,
        client_secret=CLIENT_SECRET,
        authorization_response=flask.request.url
    )

    user_info = simplelogin.get(USERINFO_URL).json()
    print(user_info['email'])
    session['email'] = user_info['email']
    return f"""
    User information: <br>
    Name: {user_info["name"]} <br>
    Email: {user_info["email"]} <br>
    Avatar <img src="{user_info.get('avatar_url')}"> <br>
    <br>
    <a href="/reviews">reviews</a> <br>
    <a href="/">Home</a>
    """

@app.route('/reviews')
def all_reviews():
    if 'email' not in session:
        return redirect(url_for('/'))
    else:
        return fetch_user_reviews(session['email'])

@app.route('/review/<id>')
def get_reveiew(id):
    try:
        return jsonify(fetch_review(id))
    except NotFoundError:
        abort(404, description='Resource not found')
    except NotAuthorizedError:
        abort(403, description='Access Denied')

if __name__ == '__main__':
    app.run(debug=True)