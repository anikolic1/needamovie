from flask import Flask, request, jsonify
from flask_cors import CORS
from scraper import scrape_profile
from recommender import get_movie_recs
from omdb_client import get_movie_info

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route("/")
def home():
    return "Backend operational", 200

# endpoint for scraping
@app.route("/api/scrape", methods=["POST"])
def api_scrape():
    data = request.get_json()
    username = data.get("userName")
    max_movies = 500

    # scrape the profile, returns list of dicts of highest rated movies
    scraped_data, error = scrape_profile(username, max_movies)
    if error:
        return jsonify({"error": error}), 400
    # get recommended movies based on scraped movies
    movie_recs = get_movie_recs(scraped_data["movies"])

    # now add additional info to each movie rec, such as genre, director, etc
    final_movie_recs = []
    for movie in movie_recs:
        extra_info = get_movie_info(movie["title"], movie["year"])
        final_movie = {**movie, **extra_info}
        final_movie_recs.append(final_movie)

    # return recommended movies as a list of dicts with title, year, reason
    return jsonify(final_movie_recs)