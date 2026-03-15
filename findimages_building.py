import json
import os

from dotenv import load_dotenv
from serpapi.google_search import GoogleSearch

load_dotenv()

secret_key = os.getenv("SECRET_KEY")
buildings = []
updated_buildings = []

try:
    with open("public/data/accurate_buildings.json", "r", encoding="utf-8") as file:
        buildings = json.load(file)
except Exception as error:
    print(f"An error occurred: {error}")

for building in buildings:
    words = building["description"].split()
    name = " ".join(words[:4]) + " Basking Ridge, NJ"
    params = {
        "engine": "google_images",
        "q": name,
        "location": "Basking Ridge, New Jersey, United States",
        "google_domain": "google.com",
        "hl": "en",
        "gl": "us",
        "api_key": secret_key,
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    image = results["images_results"][0]["original"]
    updated_buildings.append({**building, "name": name, "image": image})

with open("public/data/accurate_buildings.json", "w", encoding="utf-8") as file:
    json.dump(updated_buildings, file, indent=4)
