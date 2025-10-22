from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import requests

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
        # Using DuckDuckGo API (no key needed)
        url = f"https://api.duckduckgo.com/?q={query}&format=json&no_redirect=1"
        response = requests.get(url)
        data = response.json()

        results = []
        if "RelatedTopics" in data:
            for item in data["RelatedTopics"]:
                if "Text" in item and "FirstURL" in item:
                    results.append({
                        "title": item["Text"],
                        "url": item["FirstURL"]
                    })

        return {"query": query, "results": results}

    except Exception as e:
        return {"error": str(e)}
