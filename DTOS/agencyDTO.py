from pydantic import BaseModel
from typing import List

# ✅ Basic DTO for Agencies (without related players)
class AgencyDTO(BaseModel):
    id: int
    Agencyname: str
    Agencyverified: bool

    class Config:
        from_attributes = True  # Enables conversion from SQLAlchemy ORM objects

