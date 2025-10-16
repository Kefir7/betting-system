# app/models.py
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .db import Base
import copy

class Match(Base):
    __tablename__ = "matches"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=datetime.utcnow)
    home_team = Column(String)
    away_team = Column(String)
    home_goals = Column(Integer, nullable=True)
    away_goals = Column(Integer, nullable=True)
    result = Column(String, nullable=True)

    def clone(self):
        return copy.deepcopy(self)

class Odds(Base):
    __tablename__ = "odds"
    id = Column(Integer, primary_key=True, index=True)
    match_id = Column(Integer, ForeignKey("matches.id"))
    home = Column(Float)
    draw = Column(Float)
    away = Column(Float)
    provider = Column(String, default="demo")
    match = relationship("Match", backref="odds")
