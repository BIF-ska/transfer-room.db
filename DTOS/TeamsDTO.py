from pydantic import BaseModel
from typing import Optional

class TeamDTO(BaseModel):
    Team_id: int
    Teamname: str
    Competition_id: Optional[int] = None  # Foreign key reference to Competition
    Country_id: Optional[int] = None  # Foreign key reference to Country

    class Config:
        from_attributes = True  # Enables conversion from SQLAlchemy ORM objects
