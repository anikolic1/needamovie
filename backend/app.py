from flask import Flask, request, jsonify
from flask_cors import CORS

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
    scraped_data, error = scrape_profile_data(username)
    if error:
        return jsonify({"error": error}), 400
    return jsonify({"message":f"Received Username: {username}"})

def scrape_profile_data(username):
    # for now, just return the username
    try:
        if not username:
            return None, "No username provided"
        # scraper logic here
        return {"username": username}, None
    except Exception as e:
        return None, str(e)