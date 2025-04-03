from pydantic import BaseModel
from typing import Optional

class TeamDTO(BaseModel):
    Team_id: int
    Teamname: str
    Competition_id: Optional[int] = None
    Country_id: Optional[int] = None 

    class Config:
        from_attributes = True  
