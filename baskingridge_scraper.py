import json
import re
import time

import requests
from bs4 import BeautifulSoup


def scrape_basking_ridge_full():
    url = "https://en.wikipedia.org/wiki/Basking_Ridge,_New_Jersey"
    headers = {"User-Agent": "Mozilla/5.0"}

    print("Fetching full historical text...")

    try:
        response = requests.get(url, headers=headers, timeout=30)
        time.sleep(1)

        if response.status_code != 200:
          print(f"Error: {response.status_code}")
          return

        soup = BeautifulSoup(response.text, "html.parser")
        content = soup.find("div", {"id": "mw-content-text"})
        full_date_pattern = re.compile(
            r"((?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4})|(\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4})|(\b(17|18|19|20)\d{2}\b)"
        )

        results = []

        for element in content.find_all(["li"]):
            text = element.get_text().strip()
            match = full_date_pattern.search(text)

            if match and len(text) > 40:
                clean_description = re.sub(r"\[\d+\]", "", text).replace("\n", " ")
                results.append(
                    {
                        "date": match.group(0),
                        "description": clean_description,
                    }
                )

        unique_results = []
        seen = set()

        for item in results:
            key = item["description"][:60]
            if key not in seen:
                unique_results.append(item)
                seen.add(key)

        people_results = [item for item in unique_results if "(born" in item["description"]]
        building_results = [item for item in unique_results if "built" in item["description"]]

        with open("public/data/accurate_events.json", "w", encoding="utf-8") as file:
            json.dump(unique_results, file, indent=4)
        with open("public/data/accurate_people.json", "w", encoding="utf-8") as file:
            json.dump(people_results, file, indent=4)
        with open("public/data/accurate_buildings.json", "w", encoding="utf-8") as file:
            json.dump(building_results, file, indent=4)

        print(f"Success! Saved {len(unique_results)} events.")

    except Exception as error:
        print(f"An error occurred: {error}")


if __name__ == "__main__":
    scrape_basking_ridge_full()
