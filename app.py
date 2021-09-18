import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, abort, jsonify, make_response
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VideoGrant

app = Flask(__name__)

profile = {
    "name": "Annie Liu",
    "age": 20,
    "address": "2205 Lower Mall",
    "emergency contact": "Linda Ma",
    "allergies": [],
    "blood type": "AB",
    "conditions": [],
    "medications": [],
    "BMI": 3,
    "height": 165,
    "weight": 50
}


@app.route("/")
def profile():
    return "profile settings"


@app.route("/userinfo", methods=["GET"])
def retrieve():
    return profile


load_dotenv()
twilio_account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
twilio_api_key_sid = os.environ.get("TWILIO_API_KEY_SID")
twilio_api_key_secret = os.environ.get("TWILIO_API_KEY_SECRET")


@app.route("/video")
def index():
    return render_template("vidchat.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.get_json(force=True).get("username")
    if not username:
        abort(401)

    token = AccessToken(
        twilio_account_sid, twilio_api_key_sid, twilio_api_key_secret, identity=username
    )
    token.add_grant(VideoGrant(room="My Room"))

    return {"token": token.to_jwt().decode()}

@app.route("/signup", methods=["POST", "GET"])
def signup():
    if not all(userField in request.json for userField in ("name", "age", "address", "emergency contact", "blood type", "BMI", "height", "weight")):
        abort(400, description="Resource not found")
    if not (field is str for field in ("name", "address", "emergency contact", "blood type")):
        abort(400, description="Keys are supposed to be string")
    if not (field is int or float for field in ("age", "BMI", "weight", "height")):
        abort(400, description="Keys are supposed to be numbers")

    profile['name'] = request.json['name']
    profile['age'] = request.json['age']
    profile['address'] = request.json['address']
    profile['emergency contact'] = request.json['emergency contact']
    profile['allergies'] = request.json['allergies']
    profile['blood type'] = request.json['blood type']
    profile['conditions'] = request.json['conditions']
    profile['medications'] = request.json['medications']
    profile['BMI'] = request.json['BMI']
    profile['height'] = request.json['height']
    profile['weight'] = request.json['weight']

    return jsonify(result = "Account created!")

@app.route('/edit', methods=['PUT', "GET"])
def edit():
    if not all(userField in request.json for userField in ("name", "age", "address", "emergency contact", "blood type", "BMI", "height", "weight")):
        abort(400, description="Resource not found")
    if not (field is str for field in ("name", "address", "emergency contact", "blood type")):
        abort(400, description="Keys are supposed to be string")
    if not (field is int or float for field in ("age", "BMI", "weight", "height")):
        abort(400, description="Keys are supposed to be numbers")

    profile['name'] = request.json.get(['name'], profile['name'])
    profile['age'] = request.json.get(['age'], profile['age'])
    profile['address'] = request.json.get(['address'],profile['address'])
    profile['emergency contact'] = request.json.get(['emergency contact'],profile['emergency contact'])
    profile['allergies'] = request.json.get(['allergies'],  profile['allergies'])
    profile['blood type'] = request.json.get(['blood type'], profile['blood type'])
    profile['conditions'] = request.json.get(['conditions'], profile['conditions'] )
    profile['medications'] = request.json.get(['medications'], profile['medications'])
    profile['BMI'] = request.json.get(['BMI'], profile['BMI'])
    profile['height'] = request.json.get(['height'], profile['height'])
    profile['weight'] = request.json.get(['weight'], profile['weight'])
    
    return jsonify({'profile': profile}, result = "Successfully edited!")

if __name__ == "__main__":
    app.run(debug=True)
