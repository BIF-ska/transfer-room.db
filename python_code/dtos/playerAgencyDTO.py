from pydantic import BaseModel
from typing import List



# ✅ DTO for PlayerAgency (Only Foreign Keys)
class PlayerAgencyDTO(BaseModel):
    Player_id: int
    Agency_id: int

    class Config:
        from_attributes = True

