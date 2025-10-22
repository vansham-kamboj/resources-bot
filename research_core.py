import json
import random

# Path to pre-fetched resources JSON
RESOURCE_FILE = "pre_fetched_resources.json"

def load_resources():
    """
    Load pre-fetched resources from JSON file.
    JSON structure:
    {
        "ReactJS": [
            {"title": "...", "link": "...", "snippet": "...", "type": "Web"},
            {"title": "...", "link": "...", "snippet": "...", "type": "YouTube"}
        ],
        "Python": [...]
    }
    """
    try:
        with open(RESOURCE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except Exception as e:
        print("Error loading resources:", e)
        return {}

def search_educational_resources(query, max_web=6, max_youtube=5):
    """
    Search resources from pre-fetched JSON.
    Returns combined list of Web + YouTube resources.
    """
    all_resources = load_resources()
    results = []

    # Case-insensitive match of query with keys
    matched_topics = [
        topic for topic in all_resources.keys()
        if query.lower() in topic.lower()
    ]

    for topic in matched_topics:
        resources = all_resources[topic]
        # Separate Web and YouTube
        web_res = [r for r in resources if r["type"] == "Web"][:max_web]
        yt_res = [r for r in resources if r["type"] == "YouTube"][:max_youtube]
        results.extend(web_res + yt_res)

    # If nothing matched, optionally return random resources
    if not results:
        all_items = [r for resources in all_resources.values() for r in resources]
        results = random.sample(all_items, min(max_web + max_youtube, len(all_items)))

    return results

def fetch_page_snippet(url, max_chars=300):
    """
    Optional: Not used in pre-fetched version.
    Kept for compatibility with app.py
    """
    return "Snippet unavailable in pre-fetched mode."
