from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, BigInteger
from sqlalchemy.orm import relationship
from models import Base
from datetime import datetime


columns_dict = {
    "Agency_id": Column(Integer, ForeignKey=True),
    "player_id": Column(Integer, ForeignKey=True),
    }


class Playeragencies(Base):
  
    __tablename__ = "player_agencies"
    Agency_id = Column(Integer, ForeignKey("agencies.id"))
    player_id = Column(Integer, ForeignKey("players.id"))

    # Relationships
    player = relationship("Player")
    agency = relationship("Agency")

    def __repr__(self):
        return f"Playeragencies(player_id={self.player_id!r}, Agency_id={self.Agency_id!r})"


    