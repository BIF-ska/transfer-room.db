from pydantic import BaseModel
from typing import List, Optional

class CountryDTO(BaseModel):
    Country_id: int
    Name: str

    class Config:
        from_attributes = True  # Enables conversion from SQLAlchemy ORM objects
