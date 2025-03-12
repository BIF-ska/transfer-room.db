from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, BigInteger, Date, Enum
from sqlalchemy.orm import relationship
from .base import Base



class teamHistory(Base):
    __tablename__ = 'team_history'

    team_history_id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('players.player_id'))
    name = Column(String(100))
    from_team = Column(String(255))
    to_team = Column(String(255))
    start_date = Column(Date)
    end_date = Column(Date)
    transfer_type = Column(String(50))
    transfer_fee_euros = Column(Float)
    created_at = Column(DateTime)

