from sqlalchemy import Column, Integer, VARCHAR, Boolean, ForeignKey, Date, Enum, String, Float 
from sqlalchemy.orm import relationship
from .base import Base




class Players(Base):
    __tablename__ = 'players'

    player_id = Column(Integer, primary_key=True)
    player_name = Column(String(100))
    tr_id = Column(Integer)
    birth_date = Column(Date)
    first_position = Column(String(100))
    nationality1 = Column(String(100))
    nationality2 = Column(String(100), nullable=True)
    parent_team = Column(String(100))
    competition_id = Column(Integer, ForeignKey('competition.competition_id'))
    fk_team_id = Column(Integer, ForeignKey('team.team_id'))
    fk_country_id = Column(Integer, ForeignKey('country.country_id'))

    agencies = relationship("playerAgency", back_populates="player")
