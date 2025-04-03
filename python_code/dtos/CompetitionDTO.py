from pydantic import BaseModel
from typing import Optional

class CompetitionDTO(BaseModel):
    Competition_id: int
    Competitionname: str
    divisionLevel: int
    country_fk_id: Optional[int] = None 

    class Config:
        from_attributes = True  
