from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..db import SessionLocal

router = APIRouter(prefix="/matches", tags=["matches"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.MatchResponse)
def create_match(match: schemas.MatchCreate, db: Session = Depends(get_db)):
    return crud.create_match(db, match)

@router.get("/", response_model=list[schemas.MatchResponse])
def read_matches(db: Session = Depends(get_db)):
    return crud.get_matches(db)
