# app/db.py
from config import settings
print(f"DATABASE_URL RAW: {settings.DATABASE_URL!r}")


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import settings

class EngineSingleton:
    _instance = None

    @staticmethod
    def get_instance():
        if EngineSingleton._instance is None:
            EngineSingleton._instance = create_engine(settings.DATABASE_URL)
        return EngineSingleton._instance

engine = EngineSingleton.get_instance()
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
def init_db():
    from app import models
    Base.metadata.create_all(bind=engine)