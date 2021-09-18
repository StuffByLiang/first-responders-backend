from flask import Flask, render_template, request, jsonify, make_response, abort

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


