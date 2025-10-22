from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import requests
import urllib.parse

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "FastAPI Search API running!"}


@app.get("/search")
def search_topic(query: str = Query(..., min_length=1)):
    try:
        url = f"https://api.duckduckgo.com/?q={query}&format=json&no_redirect=1"
        response = requests.get(url)
        data = response.json()

        results = []
        if "RelatedTopics" in data:
            for item in data["RelatedTopics"]:
                if "Text" in item and "FirstURL" in item:
                    clean_url = item["FirstURL"]
                    # Decode any redirect or encoded URL (DuckDuckGo returns encoded links)
                    if "uddg=" in clean_url:
                        parsed = urllib.parse.parse_qs(urllib.parse.urlparse(clean_url).query)
                        if "uddg" in parsed:
                            clean_url = parsed["uddg"][0]
                    clean_url = urllib.parse.unquote(clean_url)

                    results.append({
                        "title": item["Text"],
                        "url": clean_url
                    })

        return {"query": query, "results": results}

    except Exception as e:
        return {"error": str(e)}
