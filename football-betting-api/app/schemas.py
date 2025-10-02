from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class MatchBase(BaseModel):
    home_team: str
    away_team: str
    date: Optional[datetime] = None

class MatchCreate(MatchBase):
    pass

class MatchResponse(MatchBase):
    id: int
    model_config = {
        "from_attributes": True
    }

class OddsBase(BaseModel):
    home: float
    draw: float
    away: float
    provider: Optional[str] = "demo"

class OddsCreate(OddsBase):
    match_id: int

class OddsResponse(OddsCreate):
    id: int
    model_config = {
        "from_attributes": True
    }
