import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, abort, jsonify, make_response
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VideoGrant

app = Flask(__name__)

profile = {
    'name': "Annie Liu",
    'age': "20",
    'address': "2205 Lower Mall",
    'emergency contact': "Linda Ma",
    'allergies': [],
    'blood type': "AB",
    'conditions': [],
    'medications': [],
    'BMI': 3,
    'height': 165,
    'weight': 50
}

@app.route("/")
def profile():
    return "profile settings"

@app.route('/userinfo', methods = ['GET'])
def retrieve():
    return jsonify({'profile': profile})

load_dotenv()
twilio_account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
twilio_api_key_sid = os.environ.get('TWILIO_API_KEY_SID')
twilio_api_key_secret = os.environ.get('TWILIO_API_KEY_SECRET')

@app.route('/video')
def index():
    return render_template('vidchat.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.get_json(force=True).get('username')
    if not username:
        abort(401)

    token = AccessToken(twilio_account_sid, twilio_api_key_sid,
                        twilio_api_key_secret, identity=username)
    token.add_grant(VideoGrant(room='My Room'))

    return {'token': token.to_jwt().decode()}

if __name__ == "__main__":
    app.run(debug=True)
