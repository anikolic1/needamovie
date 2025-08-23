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
    
    movies = []
    page = 1

    # loop through the pages of the user's profile
    # only scrapes up to max_movies, or less if it encounters an empty page
    while len(movies) < max_movies:
        url = f"{BASE_URL}/{username}/films/by/entry-rating/page/{page}/"

        # get request to the user's list of movies sorted by highest rated for current page
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            if response.status_code != 200:
                return None, f"Failed to fetch profile (status code {response.status_code})"
        except Exception as e:
            return None, str(e)
        
        # need edge cases like private profile, etc
        soup = BeautifulSoup(response.text, "html.parser")

        # select all the movies shown on this page
        movie_blocks = soup.select("ul.grid li")
        # no more movies, page will be blank, break
        if not movie_blocks:
            break

        for block in movie_blocks:
            # stop scraping if max_movies is reached
            if len(movies) >= max_movies:
                break

            poster_div = block.find("div", class_="react-component")
            if not poster_div:
                continue

            # movie title
            img = poster_div.find("img")
            title = img.get("alt") if img else None

            # movie rating
            # the rating is stored in the class name of a span tag, need to extract
            rating_span = block.find("span", class_="rating")
            rating = None
            if rating_span:
                # loop through each class in the span until the rating-X class
                for span_class in rating_span.get("class", []):
                    if span_class.startswith("rated-"):
                        # extract the rating number from the class name
                        try:
                            rating = int(span_class.split("-")[1]) / 2
                            break
                        except ValueError:
                            continue

            # if it's a valid movie, append to list of dicts for each movie
            if title and rating is not None:
                movies.append({
                    "title": title,
                    "rating": rating
                })

        # increase page count for each loop    
        page += 1

    if movies:
        return {"movies": movies}, None
    else:
        return None, "No films found on profile"