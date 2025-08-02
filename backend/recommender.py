from openai import OpenAI
import os
import json
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = "gpt-4o"
TOOLS= [{
    "type": "function",
    "name": "rec_movies",
    "description": ("Generate 5 personalized movie recommendations the user"
    "has not seen, based on the movies they have rated"),
    "parameters": {
        "type": "object",
        "properties": {
            "recommendations": {
                "type": "array",
                "minItems": 5,
                "maxItems": 5,
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
            "The following is a list of movies the user has rated, from "
            "0 to 5: "
            f"{json.dumps(movies)}\n"
            "Please recommend exactly 5 movies the user has NOT yet seen, "
            "each with a title (string), year (integer), and a "
            "brief reason (string)."
        )
    }

    try:
        response = client.responses.create(
            model=MODEL,
            instructions="You are a helpful movie recommender.",
            input=[user_message],
            tools=TOOLS
        )

        # tool_call = response.output[0]
        # recs = json.loads(tool_call.arguments)
        # return recs

        print(response.output)
    except Exception as e:
        print("Error calling OpenAI API:")
        print(e)