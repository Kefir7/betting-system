# app/services/football_data.py
import requests
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app import crud, schemas
from app.db import SessionLocal
from config import settings

URL = f"https://api.football-data.org/v4/competitions/{settings.FOOTBALL_COMPETITION}/matches"
HEADERS = {"X-Auth-Token": settings.FOOTBALL_API_KEY}

def fetch_matches():
    db: Session = SessionLocal()
    try:
        response = requests.get(URL, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        
        for match in data.get("matches", []):
            match_date = datetime.fromisoformat(match["utcDate"].replace("Z", "+00:00"))
            home_goals = match["score"]["fullTime"]["home"]
            away_goals = match["score"]["fullTime"]["away"]
            
            # Определяем результат
            if home_goals is not None and away_goals is not None:
                if home_goals > away_goals:
                    result = "HOME"
                elif home_goals < away_goals:
                    result = "AWAY"
                else:
                    result = "DRAW"
            else:
                result = None  # матч ещё не сыгран
            
            # Создаём объект Match
            match_create = schemas.MatchCreate(
                home_team=match["homeTeam"]["name"],
                away_team=match["awayTeam"]["name"],
                date=match_date
            )
            
            # Проверяем, есть ли матч в БД
            existing = db.query(crud.models.Match).filter(
                crud.models.Match.home_team == match_create.home_team,
                crud.models.Match.away_team == match_create.away_team,
                crud.models.Match.date == match_create.date
            ).first()
            
            if existing:
                # Обновляем результат и счет, если матч уже есть
                existing.home_goals = home_goals
                existing.away_goals = away_goals
                existing.result = result
                db.commit()
            else:
                # Создаем новый матч с результатом
                db_match = crud.models.Match(
                    home_team=match_create.home_team,
                    away_team=match_create.away_team,
                    date=match_create.date,
                    home_goals=home_goals,
                    away_goals=away_goals,
                    result=result
                )
                db.add(db_match)
                db.commit()
    finally:
        db.close()