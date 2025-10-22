from fastapi import FastAPI, Request, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from research_core import search_educational_resources, fetch_page_snippet
import os

app = FastAPI()

# Enable CORS for all origins (you can restrict this for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API endpoint supporting both GET and POST
@app.get("/research")
async def research_get(query: str):
    resources = search_educational_resources(query, max_results=8)
    for r in resources:
        r["snippet"] = fetch_page_snippet(r["link"])
    return {"original_query": query, "resources": resources}

@app.post("/research")
async def research_post(query: str = Form(...)):
    resources = search_educational_resources(query, max_results=8)
    for r in resources:
        r["snippet"] = fetch_page_snippet(r["link"])
    return JSONResponse({"original_query": query, "resources": resources})

# Optional: serve static frontend
from fastapi.staticfiles import StaticFiles
#app.mount("/", StaticFiles(directory="static", html=True), name="static")

# Uvicorn entrypoint for Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=port)
