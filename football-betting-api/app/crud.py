from sqlalchemy.orm import Session
from .import models, schemas

# Создание матча
def create_match(db: Session, match: schemas.MatchCreate):
    db_match = models.Match(
        home_team = match.home_team,
        away_team = match.away_team,
        date = match.date
    )

    db.add(db_match)
    db.commit()
    db.refresh(db_match)
    return db_match

# Получить матч по id
def get_match(db: Session, match_id: int):
    return db.query(models.Match).filter(models.Match.id == match_id).first()

# Получить все матчи
def get_matches(db: Session):
    return db.query(models.Match).all()

# Создание коэффициента
def create_odds(db: Session, odds:schemas.OddsCreate):
    db_odds = models.Odds(
        match_id = odds.match_id,
        home = odds.home,
        draw = odds.draw,
        away = odds.away,
        provider = odds.provider
    )
    
    db.add(db_odds)
    db.commit()
    db.refresh(db_odds)
    return db_odds