from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Backend operational"

@app.route("/api/scrape", methods=["POST"])
def scrape_profile():
    data = request.get_json()
    profile_url = data.get("url")
    # TODO scraper function
    return jsonify({"message":f"Received URL: {profile_url}"})