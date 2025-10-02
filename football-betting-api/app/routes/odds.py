from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..db import SessionLocal

router = APIRouter(prefix="/odds", tags=["odds"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.OddsResponse)
def create_odds(odds: schemas.OddsCreate, db: Session = Depends(get_db)):
    return crud.create_odds(db, odds)
