from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class playerAgency(Base):
    __tablename__ = "player_agency"

    player_id = Column(Integer, ForeignKey("players.player_id"), primary_key=True)
    agency_id = Column(Integer, ForeignKey("agencies.agency_id"), primary_key=True)

    # Define relationships to Players and Agencies
    player = relationship("Players", back_populates="agencies")
    agency = relationship("Agencies", back_populates="players")