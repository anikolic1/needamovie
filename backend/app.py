from flask import Flask, request, jsonify
from flask_cors import CORS
from scraper import scrape_profile
from recommender import get_movie_recs

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

    # scrape the profile, returns list of dicts of highest rated movies
    scraped_data, error = scrape_profile(username, max_movies)
    # below is a temp function call to test out the api
    movie_recs = get_movie_recs(scraped_data["movies"])

    # return recommended movies as a list of dicts with title, year, reason
    if error:
        return jsonify({"error": error}), 400
    return jsonify(movie_recs)