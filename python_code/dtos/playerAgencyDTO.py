from pydantic import BaseModel
from typing import List

class PlayerAgencyDTO(BaseModel):
    Player_id: int
    Agency_id: int

    class Config:
        from_attributes = True

