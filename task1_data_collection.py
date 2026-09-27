import requests
import time
import json
import os
from datetime import datetime
TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

# Required User-Agent
headers = {
    "User-Agent": "TrendPulse/1.0"
}
categories = {
    "technology": [
        "AI", "software", "tech", "code", "computer",
        "data", "cloud", "API", "GPU", "LLM"
    ],

    "worldnews": [
        "war", "government", "country", "president",
        "election", "climate", "attack", "global"
    ],

    "sports": [
        "NFL", "NBA", "FIFA", "sport", "game",
        "team", "player", "league", "championship"
    ],

    "science": [
        "research", "study", "space", "physics",
        "biology", "discovery", "NASA", "genome"
    ],

    "entertainment": [
        "movie", "film", "music", "Netflix", "game",
        "book", "show", "award", "streaming"
    ]
}
def matches_category(title, keywords):
    title_lower = title.lower()

    for keyword in keywords:
        if keyword.lower() in title_lower:
            return True

    return False
print("TrendPulse - Task 1")
print("Starting data collection...")

try:
    response = requests.get(
        TOP_STORIES_URL,
        headers=headers,
        timeout=10
    )

    response.raise_for_status()

    story_ids = response.json()[:500]

    print(f"Found {len(story_ids)} story IDs.")

except requests.RequestException as error:
    print("Could not get the list of story IDs.")
    print("Error:", error)
    exit()
stories = []

category_counts = {
    "technology": 0,
    "worldnews": 0,
    "sports": 0,
    "science": 0,
    "entertainment": 0
}
for category, keywords in categories.items():

    print()
    print(f"Collecting {category} stories...")

    for story_id in story_ids:

        # Stop when this category has 25 stories
        if category_counts[category] >= 25:
            break

        url = ITEM_URL.format(story_id)

        try:
            response = requests.get(
                url,
                headers=headers,
                timeout=10
            )

            response.raise_for_status()

            story = response.json()

        except requests.RequestException as error:
            print(f"Could not fetch story {story_id}: {error}")
            continue

        # Ignore empty results
        if story is None:
            continue

        title = story.get("title", "")

        # Ignore stories without titles
        if not title:
            continue

        # Check whether this title matches this category
        if not matches_category(title, keywords):
            continue

        # Create the seven required fields
        story_data = {
            "post_id": story.get("id"),
            "title": title,
            "category": category,
            "score": story.get("score", 0),
            "num_comments": story.get("descendants", 0),
            "author": story.get("by"),
            "collected_at": datetime.now().isoformat()
        }

        stories.append(story_data)
        category_counts[category] += 1

        print(
            f"Collected {category_counts[category]}/25: {title}"
        )

    # Required 2-second wait between category loops
    time.sleep(2)
os.makedirs("data", exist_ok=True)
date_string = datetime.now().strftime("%Y%m%d")
filename = f"data/trends_{date_string}.json"
with open(filename, "w", encoding="utf-8") as file:

    json.dump(
        stories,
        file,
        indent=4,
        ensure_ascii=False
    )
print()
print("----------------------------------------")
print(f"Total stories collected: {len(stories)}")
print(f"Saved to: {filename}")
print("Category counts:")

for category, count in category_counts.items():
    print(f"{category}: {count}")

print("----------------------------------------")
print("Task 1 completed.")