from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
from research_core import search_educational_resources, fetch_page_snippet

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/research")
async def research_endpoint(query: str = Form(...)):
    resources = search_educational_resources(query, web_results=6, youtube_results=5)
    # Optional: fetch snippets for web
    for r in resources:
        if r["type"] == "Web":
            r["snippet"] = fetch_page_snippet(r["link"])
    return JSONResponse({"original_query": query, "resources": resources})
