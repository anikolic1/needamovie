from openai import OpenAI
import os
import json
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL_VER = "gpt-4o"

## returns movie recs from OpenAI GPT, passed in scraped movies from
## the user profile
def get_movie_recs(movies):
    try:
        response = client.responses.create(
            model=MODEL_VER,
            instructions="You are a helpful movie recommender.",
            input="I really like Parasite(2019), what else should I watch?",
        )

        print(response.output_text)
    except Exception as e:
        print("Error calling OpenAI API:")
        print(e)