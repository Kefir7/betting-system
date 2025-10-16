# app/services/football_data.py
import requests
from datetime import datetime
from sqlalchemy.orm import Session
from app import crud, schemas
from app.db import SessionLocal
from config import settings

# Паттерны
from app.patterns.observer import MatchSubject, BettingService
from app.patterns.strategy import calculate_win
from app.patterns.chain import BalanceCheck, BetLimitCheck
from app.patterns.command import Scheduler, FetchMatchesCommand
from app.patterns.adapter import PaymentAdapter, OldPaymentSystem

URL = f"https://api.football-data.org/v4/competitions/{settings.FOOTBALL_COMPETITION}/matches"
HEADERS = {"X-Auth-Token": settings.FOOTBALL_API_KEY}

# Observer
subject = MatchSubject()
subject.attach(BettingService())

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
                result = None
            
            match_create = schemas.MatchCreate(
                home_team=match["homeTeam"]["name"],
                away_team=match["awayTeam"]["name"],
                date=match_date
            )
            
            existing = db.query(crud.models.Match).filter(
                crud.models.Match.home_team == match_create.home_team,
                crud.models.Match.away_team == match_create.away_team,
                crud.models.Match.date == match_create.date
            ).first()
            
            if existing:
                # Обновляем счёт
                existing.home_goals = home_goals
                existing.away_goals = away_goals
                existing.result = result
                db.commit()

                # Observer уведомляет подписчиков
                subject.notify(existing.id, f"{home_goals}-{away_goals}")

                # Пример Chain + Strategy + Adapter для ставки (тестовая ставка)
                user = {"id": 1, "balance": 5000, "type": "VIP"}
                bet_amount = 100
                odds = 2.5
                chain = BalanceCheck(BetLimitCheck())
                if chain.handle(user, bet_amount):
                    win = calculate_win(user["type"], bet_amount, odds)
                    adapter = PaymentAdapter(OldPaymentSystem())
                    adapter.pay(user, win)
            else:
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
                # Observer уведомляет о новом матче
                subject.notify(db_match.id, f"{home_goals}-{away_goals}")

                # Тот же пример для Chain + Strategy + Adapter
                user = {"id": 1, "balance": 5000, "type": "VIP"}
                bet_amount = 100
                odds = 2.5
                chain = BalanceCheck(BetLimitCheck())
                if chain.handle(user, bet_amount):
                    win = calculate_win(user["type"], bet_amount, odds)
                    adapter = PaymentAdapter(OldPaymentSystem())
                    adapter.pay(user, win)

    finally:
        db.close()
