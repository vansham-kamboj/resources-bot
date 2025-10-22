import requests
from bs4 import BeautifulSoup

def search_educational_resources(query: str, num_web_results=6, num_youtube_results=5):
    results = {"web": [], "youtube": []}

    # --- Web Results (DuckDuckGo HTML search) ---
    url = f"https://duckduckgo.com/html/?q={query}"
    res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(res.text, "html.parser")

    for link in soup.select(".result__a")[:num_web_results]:
        results["web"].append({
            "title": link.get_text(),
            "url": link["href"]
        })

    # --- YouTube Results (Google search restricted to youtube.com) ---
    yt_url = f"https://www.google.com/search?q=site:youtube.com+{query}+hindi+english"
    yt_res = requests.get(yt_url, headers={"User-Agent": "Mozilla/5.0"})
    yt_soup = BeautifulSoup(yt_res.text, "html.parser")

    for g in yt_soup.select("a")[:num_youtube_results]:
        href = g.get("href", "")
        if "youtube.com/watch" in href:
            results["youtube"].append({
                "title": g.get_text() or "YouTube Video",
                "url": href
            })

    return results
