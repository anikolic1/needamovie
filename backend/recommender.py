from openai import OpenAI
import os
import json
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
NUM_RECS = 6
MODEL = "gpt-5"
TOOLS= [{
    "type": "function",
    "name": "rec_movies",
    "description": (
        f"Generate {NUM_RECS} personalized movie recommendations the user based on the movies they have rated. "
        "Strictly DO NOT recommend any movies the user has already rated. "
        "Check the provided list carefully before generating recommendations. "
        "Each recommendation must include a title (string), year (integer), and a brief reason (string)."
        ),
    "parameters": {
        "type": "object",
        "properties": {
            "recommendations": {
                "type": "array",
                "minItems": NUM_RECS,
                "maxItems": NUM_RECS,
                "items": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "year": {"type": "integer"},
                        "reason": {"type": "string"}
                    },
                    "required": ["title", "year", "reason"]
                }
            }
        },
        "required": ["recommendations"]
    }
}]

## returns movie recs from OpenAI GPT, passed in scraped movies from
## the user profile, using OpenAI GPT with function calling
def get_movie_recs(movies):
    user_message = {
        "role": "user",
        "content": (
            "The following is a list of movies the user has already rated, from 0 to 5"
            f"{json.dumps(movies)}\n"
            f"Please recommend exactly {NUM_RECS} movies the user has NOT yet seen, "
            "each with a title (string), year (integer), and a brief reason (string). "
            "Do NOT include any movie from the above list."
        )
    }

    try:
        response = client.responses.create(
            model=MODEL,
            instructions="You are a helpful movie recommender.",
            input=[user_message],
            tools=TOOLS
        )

        # loop over response blocks to find tool_calls and extract the recs
        recs = []
        for item in response.output:
            if getattr(item, "type", None) == "function_call" and getattr(item, "name", None) == "rec_movies":
                args = json.loads(item.arguments)
                recs = args["recommendations"]
                break
        
        # GPT has a tendency to recommend already seen movies, so filter those out
        final_recs = []
        seen_movies = {movie["title"].lower() for movie in movies}
        for rec in recs:
            if rec["title"].lower() not in seen_movies:
                final_recs.append(rec)

        return final_recs
    except Exception as e:
        print("Error calling OpenAI API:")
        print(e)
        return []