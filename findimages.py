import json
import os

from dotenv import load_dotenv
from serpapi.google_search import GoogleSearch

load_dotenv()

secret_key = os.getenv("SECRET_KEY")
people = []
updated_people = []

try:
    with open("data/source/accurate_people.json", "r", encoding="utf-8") as file:
        people = json.load(file)
except Exception as error:
    print(f"An error occurred: {error}")

for person in people:
    name = person["description"].split("(")[0].strip()
    params = {
        "engine": "google_images",
        "q": name,
        "location": "Austin, Texas, United States",
        "google_domain": "google.com",
        "hl": "en",
        "gl": "us",
        "api_key": secret_key,
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    image = results["images_results"][0]["original"]
    updated_people.append({**person, "name": name, "image": image})

with open("public/data/accurate_people.json", "w", encoding="utf-8") as file:
    json.dump(updated_people, file, indent=4)
