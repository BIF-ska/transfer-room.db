from pydantic import BaseModel
from typing import Optional

class CompetitionDTO(BaseModel):
    Competition_id: int
    Competitionname: str
    divisionLevel: int
    country_fk_id: Optional[int] = None  # Foreign key reference to Country

    class Config:
        from_attributes = True  # Enables conversion from SQLAlchemy ORM objects
