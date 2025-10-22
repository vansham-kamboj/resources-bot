from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from research_core import search_educational_resources

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"status": "running", "message": "Welcome to Research Bot API"}

@app.post("/search")
async def research_endpoint(query: str = Form(...)):
    print("Received query:", query)
    resources = search_educational_resources(query, num_web_results=6, num_youtube_results=5)
    return resources
