from pydantic import BaseModel

# ✅ DTO for Agencies
class AgencyDTO(BaseModel):
    id: int
    Agencyname: str
    Agencyverified: bool

    class Config:
        from_attributes = True  # Enables conversion from SQLAlchemy ORM objects
