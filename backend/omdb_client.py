import os
import requests
from dotenv import load_dotenv

load_dotenv()
OMDB_API_KEY = os.getenv("OMDB_API_KEY")
OMDB_BASE_URL = "http://www.omdbapi.com/"

# this function gets additional info for a movie based on title and year
# info includes director, poster image, plot description, etc
def get_movie_info(title, year=None):

    # params for the get request, omdbapi.com is expecting certain fields
    params = {
        "apikey": OMDB_API_KEY,
        "t": title,
        "type": "movie"
    }
    # if the year was provided, add to params
    if year:
        params["y"] = year

    # get request to omdb. afterwards, return desired data
    try:
        response = requests.get(OMDB_BASE_URL, params=params)
        data = response.json()
        if data.get("Response") == "True":
            imdbid = data.get("imdbID")
            return {
                "poster": data.get("Poster"),
                "director": data.get("Director"),
                "genre": data.get("Genre"),
                "movie_url": f"https://www.imdb.com/title/{imdbid}" if imdbid else None
            }
        else:
            return {"poster": None, "director": None, "genre": None}
    except Exception as e:
        print(f"OMDb request failed for {title}: {e}")
        return {"poster": None, "director": None, "genre": None} 