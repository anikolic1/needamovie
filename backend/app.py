from flask import Flask, request, jsonify
from flask_cors import CORS
from scraper import scrape_profile

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Backend operational"

# endpoint for scraping
@app.route("/api/scrape", methods=["POST"])
def api_scrape():
    data = request.get_json()
    username = data.get("userName")
    max_movies = 15
    scraped_data, error = scrape_profile(username, max_movies)

    # for now, just returning some info of the first movie on the profile
    if error:
        return jsonify({"error": error}), 400
    return jsonify({"message":f"Movie URL: {scraped_data['movie_url']}"})