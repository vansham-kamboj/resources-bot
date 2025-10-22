from ddgs import DDGS
import requests
from bs4 import BeautifulSoup
import time

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ResourceBot/1.0"

def search_educational_resources(query, max_results=8, pause=0.2):
    """
    Searches DuckDuckGo for educational resources (tutorials, docs, courses, GitHub, YouTube)
    """
    resources = []
    keywords = ["tutorial", "docs", "course", "github", "video", "roadmap", "guide"]

    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=max_results):
            link = r.get("href")
            title = r.get("title") or link
            body = r.get("body") or ""
            if any(k.lower() in title.lower() + body.lower() for k in keywords):
                resources.append({
                    "title": title,
                    "link": link,
                    "snippet": body[:200]
                })
            time.sleep(pause)
    return resources

def fetch_page_snippet(url, max_chars=300):
    try:
        headers = {"User-Agent": USER_AGENT}
        resp = requests.get(url, headers=headers, timeout=6)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        text = " ".join([p.get_text(strip=True) for p in soup.find_all("p")])
        return text[:max_chars]
    except:
        return ""
