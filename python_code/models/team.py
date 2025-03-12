from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from .base import Base



class Teams(Base):
    __tablename__ = "team"
    
    team_id = Column(Integer, primary_key=True, autoincrement=True)
    team_name = Column(String(100))
    competition_id = Column(Integer, ForeignKey("competition.competition_id"))
    country_id = Column(Integer, ForeignKey("country.country_id"))
    

