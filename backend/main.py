from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from routers import papers

app = FastAPI()

app.include_router(papers.router)

@app.get("/")
async def health_check():
    return {"status": "ok"}
