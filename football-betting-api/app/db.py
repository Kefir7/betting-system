from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql+psycopg2://postgres:Grekov1907@localhost:5432/football_betting"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

def init_db():
    from .models import Match, Odds  # Импорт моделей здесь
    Base.metadata.create_all(bind=engine)
