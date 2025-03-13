from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime  
from .base import Base
 
 
 
class playerhistory(Base):
    __tablename__ = "player_history"
 
    player_history_id = Column(Integer, primary_key=True, autoincrement=True)
    player_id = Column(Integer, ForeignKey("players.player_id"), nullable=False)
    name= Column(String(255), nullable=False)
    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    xTV = Column(Numeric(18, 2), nullable=False)
    UpdatedAt = Column(DateTime, default=datetime.utcnow, nullable=False)  # ✅ Corrected
 
   
    # Relationship with Players Table
    player = relationship("Players", back_populates="history")
