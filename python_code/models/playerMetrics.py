from sqlalchemy import Column, Integer, String, ForeignKey, Date, Numeric
from sqlalchemy.orm import relationship
from .base import Base


# Defining the PlayerMetrics model
class playerMetrics(Base):
    __tablename__ = 'player_metrics'

    metrics_id = Column(Integer, primary_key=True, autoincrement=True)
    player_id = Column(Integer, ForeignKey('players.player_id'), nullable=False, unique=True)
    playing_style = Column(String(100), nullable=True)
    xTV = Column(Numeric(18, 0), nullable=True)
    rating = Column(Numeric(18, 0), nullable=True)
    potential = Column(Numeric(18, 0), nullable=True)
    GBE_result = Column(String(100), nullable=True)
    GBE_score = Column(Integer, nullable=True)
    base_value = Column(Numeric(18, 0), nullable=True)
    estimated_salary = Column(Numeric, nullable=True)
    contract_expiry = Column(Date, nullable=True)


    player = relationship("Players", back_populates="metrics")