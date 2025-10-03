# app/db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ------------------ Singleton ------------------
class EngineSingleton:
    _instance = None

    @staticmethod
    def get_instance(database_url):
        if EngineSingleton._instance is None:
            EngineSingleton._instance = create_engine(database_url)
        return EngineSingleton._instance

DATABASE_URL = "postgresql+psycopg2://postgres:Grekov1907@localhost:5432/football_betting"
engine = EngineSingleton.get_instance(DATABASE_URL)

# ------------------ Factory Method ------------------
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
