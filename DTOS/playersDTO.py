from pydantic import BaseModel
from typing import Optional
from datetime import date
from decimal import Decimal


class PlayerDTO(BaseModel):
    PlayerID: int
    Name: str
    BirthDate: date
    FirstPosition: str
    Nationality1: str
    Nationality2: Optional[str] = None
    ParentTeam: str
    Rating: Decimal
    Transfervalue: Decimal
    Competition_id: Optional[int] = None
    fk_players_team: Optional[int] = None

    class Config:
        from_attributes = True  # Enables conversion from SQLAlchemy ORM objects
