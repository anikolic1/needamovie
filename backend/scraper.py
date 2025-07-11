import requests
from bs4 import BeautifulSoup

BASE_URL = "https://letterboxd.com"
HEADERS = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/137.0.0.0 Safari/537.36"
            ),
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": (
                "text/html,application/xhtml+xml,application/"
                "xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,"
                "application/signed-exchange;v=b3;q=0.7"
            ),
            "Connection": "keep-alive",
        }

def scrape_profile(username, max_movies):
    if not username:
        return None, "No username provided"
    
    # get request to the user's list of movies sorted by highest rated
    url = f"{BASE_URL}/{username}/films/by/entry-rating/"
    
    # add retry logic for the get request
    # add delay to avoid spam attempts
    try:  
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code != 200:
            return None, f"Failed to fetch profile (status code {response.status_code})"
    except Exception as e:
        return None, str(e)
    
    # think of edge cases like private profiles, etc
    # for now, just getting the first movie listed
    soup = BeautifulSoup(response.text, "html.parser")
    movie = soup.select_one("div.film-poster")

    # find first poster, and get the link
    if movie and movie.has_attr("data-target-link"):
        movie_url = f"{BASE_URL}/" + movie["data-target-link"]
        return {"movie_url": movie_url}, None
    else:
        return None, "No films found on profile"