from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..db import SessionLocal

# Паттерны
from app.patterns.facade import BettingFacade
from app.patterns.observer import MatchSubject, BettingService

# Инициализация Observer
subject = MatchSubject()
subject.attach(BettingService())

# Инициализация Facade
facade = BettingFacade()

router = APIRouter(prefix="/matches", tags=["matches"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CRUD для матчей
@router.post("/", response_model=schemas.MatchResponse)
def create_match(match: schemas.MatchCreate, db: Session = Depends(get_db)):
    return crud.create_match(db, match)

@router.get("/", response_model=list[schemas.MatchResponse])
def read_matches(db: Session = Depends(get_db)):
    return crud.get_matches(db)

# Endpoint для ставок и обновления счета с паттернами
@router.post("/bet", response_model=dict)
def bet_on_match(
    match_id: int,
    new_score: str,
    user_id: int,
    bet_amount: float,
    odds: float
):
    """
    1. Обновляем счет матча в БД
    2. Срабатывает Observer для уведомлений
    3. Chain проверяет баланс и лимит
    4. Strategy считает потенциальный выигрыш
    5. Adapter проводит оплату через старую систему
    """
    # Пример пользователя (можно потом брать из БД)
    user = {"id": user_id, "balance": 5000, "type": "VIP", "is_authenticated": True}

    # Обновление матча + все паттерны
    facade.update_match_score(match_id, new_score, user, bet_amount, odds)
    return {"status": "ok"}
