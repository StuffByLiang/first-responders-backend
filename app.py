import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, abort, jsonify, make_response
from flask_cors import CORS
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VideoGrant
import uuid
from sqlalchemy.orm import sessionmaker
from sqlalchemy_cockroachdb import run_transaction
import uuid
import pickle 

from dbmain import (
    edit_account,
    get_roach_engine,
    create_account,
    query_account,
    delete_accounts,
)


app = Flask(__name__)
CORS(app)  # enable cors from all domains
engine = get_roach_engine()

## function to read serialized uuid object from file
def readFile():
    file = open('id', 'rb')
    result = pickle.load(file)
    file.close()
    return result

profile = {
    "id": readFile(),
    "name": "Annie Liu",
    "age": 20,
    "address": "2205 Lower Mall",
    "emergency_contact": "Linda Ma",
    "allergies": "",
    "blood_type": "AB", 
    "conditions": "",
    "medications": "",
    "bmi": 3,
    "height": 165,
    "weight": 50,
}


@app.route("/")
def profileSettings():
    return "profile settings"


@app.route("/userinfo", methods=["GET"])
def retrieve():
    usr_info = run_transaction(
        sessionmaker(bind=engine), lambda s: query_account(s, profile["id"])
    )
    usr_info["allergies"] = (usr_info["allergies"]).split(",")
    usr_info["conditions"] = (usr_info["conditions"]).split(",")
    usr_info["medications"] = (usr_info["medications"]).split(",")
    return jsonify(usr_info)


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
    roomname = request.get_json(force=True).get("roomname")
    if not username:
        abort(401)

    token = AccessToken(
        twilio_account_sid, twilio_api_key_sid, twilio_api_key_secret, identity=username
    )
    token.add_grant(VideoGrant(room=roomname))

    return {"token": token.to_jwt().decode()}


@app.route("/signup", methods=["POST", "GET"])
def signup():
    if not all(
        userField in request.json
        for userField in (
            "name",
            "age",
            "address",
            "emergency_contact",
            "blood_type",
            "bmi",
            "height",
            "weight",
        )
    ):
        abort(400, description="Resource not found")
    if not (
        field is str for field in ("name", "address", "emergency_contact", "blood_type")
    ):
        abort(400, description="Keys are supposed to be string")
    if not (field is int or float for field in ("age", "bmi", "weight", "height")):
        abort(400, description="Keys are supposed to be numbers")

    profile["name"] = request.json["name"]
    profile["age"] = request.json["age"]
    profile["address"] = request.json["address"]
    profile["emergency_contact"] = request.json["emergency_contact"]
    profile["allergies"] = (",").join(request.json["allergies"])
    profile["blood_type"] = request.json["blood_type"]
    profile["conditions"] = (",").join(request.json["conditions"])
    profile["medications"] =  (",").join(request.json["medications"])
    profile["bmi"] = request.json["bmi"]
    profile["height"] = request.json["height"]
    profile["weight"] = request.json["weight"]
    ## saves the account to the database
    id = run_transaction(
        sessionmaker(bind=engine), lambda s: create_account(s, profile)
    )

    return jsonify(id=id, result="Account created!")


@app.route("/edit", methods=["PUT", "GET"])
def edit():
    if not request.json:
        abort(400, description="Resource not found")
    if not (
        field is str for field in ("name", "address", "emergency_contact", "blood_type")
    ):
        abort(400, description="Keys are supposed to be string")
    if not (field is int or float for field in ("age", "bmi", "weight", "height")):
        abort(400, description="Keys are supposed to be numbers")

    profile["name"] = request.json.get("name", profile["name"])
    profile["age"] = request.json.get("age", profile["age"])
    profile["address"] = request.json.get("address", profile["address"])
    profile["emergency_contact"] = request.json.get(
        "emergency_contact", profile["emergency_contact"]
    )
    if "allergies" in request.json:
        profile["allergies"]=(",").join(request.json["allergies"])
    
    profile["blood_type"] = request.json.get("blood_type", profile["blood_type"])
    if "conditions" in request.json:
        profile["conditions"]=(",").join(request.json["conditions"])
    if "medications" in request.json:
        profile["medications"]=(",").join(request.json["medications"])
    profile["bmi"] = request.json.get("bmi", profile["bmi"])
    profile["height"] = request.json.get("height", profile["height"])
    profile["weight"] = request.json.get("weight", profile["weight"])
    run_transaction(sessionmaker(bind=engine), lambda s: edit_account(s, profile["id"], profile))

    return jsonify({"profile": profile, "result": "Successfully edited!"})


if __name__ == "__main__":
    app.run(debug=True)
