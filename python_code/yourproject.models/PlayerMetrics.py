from sqlalchemy import Column, Integer, String, ForeignKey, Date, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Defining the PlayerMetrics model
class PlayerMetrics(Base):
    __tablename__ = 'PlayerMetrics'

    MetricsID = Column(Integer, primary_key=True, autoincrement=True)
    PlayerID = Column(Integer, ForeignKey('players.PlayerID'), nullable=False)
    Salary = Column(Numeric(18, 0), nullable=True)
    ContractExpiry = Column(Date, nullable=True)
    PlayingStyle = Column(String(100), nullable=True)
    xTV = Column(Numeric(18, 0), nullable=True)
    PlayerRating = Column(Numeric(18, 0), nullable=True)
    PlayerPotential = Column(Numeric(18, 0), nullable=True)
    GBResult = Column(String(100), nullable=True)
    MinutesPlayed = Column(Numeric(18, 0), nullable=True)
    GBEScore = Column(Integer, nullable=True)
    BaseValue = Column(Numeric(18, 0), nullable=True)
    EstimatedSalary = Column(String, nullable=True)  # Using String(max) in SQLAlchemy

    # Relationships
    player = relationship("Players", back_populates="metrics")

 
 