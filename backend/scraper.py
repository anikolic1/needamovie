import requests
from bs4 import BeautifulSoup

def scrape_profile(username):
    website = "https://letterboxd.com"
    try:
        if not username:
            return None, "No username provided"
        
        # get request to the user's list of movies sorted by highest rated
        url = f"{website}/{username}/films/by/entry-rating/"
        headers = {
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

        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return None, f"Failed to fetch profile (status code {response.status_code})"

        soup = BeautifulSoup(response.text, "html.parser")

        # add retry logic for the get request
        # add delay to avoid spam attempts
        # think of edge cases like private profiles, etc
        # for now, just getting the first movie listed
        movie = soup.select_one("div.film-poster")

        # find first poster, and get the link
        if movie and movie.has_attr("data-target-link"):
            movie_url = f"{website}/" + movie["data-target-link"]
            return {"movie_url": movie_url}, None
        else:
            return None, "No films found on profile"
        
    except Exception as e:
        return None, str(e)