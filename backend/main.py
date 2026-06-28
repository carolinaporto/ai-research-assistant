from dotenv import load_dotenv

load_dotenv()

from loguru import logger
from fastapi import FastAPI
from routers import papers, folders, questions

logger.add(
    "logs/app.log",
    rotation="10 MB",
    retention="7 days",
    level="DEBUG",
)

app = FastAPI()

app.include_router(papers.router)
app.include_router(folders.router)
app.include_router(questions.router)

@app.get("/")
async def health_check():
    return {"status": "ok"}
