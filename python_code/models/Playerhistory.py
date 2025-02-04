from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, BigInteger
from sqlalchemy.orm import relationship
from models import Base
from datetime import datetime


columns_dict = {
    "Id": Column(Integer, primary_key=True),
    "player_id": Column(Integer, ForeignKey=True),
    "team_id": Column(Integer, ForeignKey=True),
    "startdate": Column(DateTime, default=datetime.utcnow),
    "enddate": Column(DateTime, default=datetime.utcnow),
    "timestamp": Column(DateTime, default=datetime.utcnow),
    "transfervalue": Column(Float),
    "last_updated": Column(DateTime),
    "create": Column(DateTime, default=datetime.utcnow),
    "update": Column(DateTime, default=datetime.utcnow),
}

class PlayerHistory(Base):
    

    
    __tablename__ = "player_history"

    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey("players.id"))
    team_id = Column(Integer, ForeignKey("teams.id"))
    startdate = Column(DateTime, default=datetime.utcnow)
    enddate = Column(DateTime, default=datetime.utcnow)
    transfervalue = Column(Float)  # Store transfer value as a float
    timestamp = Column(DateTime, default=datetime.utcnow)
    last_updated = Column(DateTime)
    create = Column(DateTime, default=datetime.utcnow)
    update = Column(DateTime, default=datetime.utcnow)

    # Relationships
    player = relationship("Player")
    team = relationship("Team")
    
    def __repr__(self):
        return f"PlayerHistory(id={self.id!r}, player_id={self.player_id!r}, team_id={self.team_id!r})"