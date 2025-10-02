#python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8080

from typing import Union
from fastapi import FastAPI
from .routes import matches, odds
from apscheduler.schedulers.background import BackgroundScheduler
from app.services.football_data import fetch_matches
from .db import init_db

app = FastAPI(title="Football Betting API")
init_db()

app.include_router(matches.router)
app.include_router(odds.router)

scheduler = BackgroundScheduler()
scheduler.add_job(fetch_matches, "interval", minutes=1)
scheduler.start()

@app.get("/")
def read_root():
    return {"status": "API is running"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
