from sqlalchemy import Column, Integer, String, ForeignKey, Date, Numeric
from sqlalchemy.orm import relationship
from decimal import Decimal

# Defining the columns dictionary for the PlayerMetrics model
columns_dict_player_metrics = {
    "MetricsID": Column(Integer, primary_key=True),
    "PlayerID": Column(Integer, ForeignKey('players.PlayerID')),
    "Salary": Column(Decimal),
    "ContractExpiry": Column(Date),
    "PlayingStyle": Column(String(100)),
    "xTV": Column(Decimal),
    "PlayerRating": Column(Decimal),
    "PlayerPotential": Column(Decimal),
    "GBEStatus": Column(String(100)),
    "MinutesPlayed": Column(Decimal)
}

# Defining the PlayerMetrics model
class PlayerMetrics(Base):
    __tablename__ = 'player_metrics'

    MetricsID = Column(Integer, primary_key=True)
    PlayerID = Column(Integer, ForeignKey('players.PlayerID'))
    Salary = Column(Decimal)
    ContractExpiry = Column(Date)
    PlayingStyle = Column(String(100))
    xTV = Column(Decimal)
    PlayerRating = Column(Decimal)
    PlayerPotential = Column(Decimal)
    GBEStatus = Column(String(100))
    MinutesPlayed = Column(Decimal)

    # Relationships
    player = relationship("Players", back_populates="metrics")

    def __repr__(self):
        return f"PlayerMetrics(MetricsID={self.MetricsID!r}, PlayerID={self.PlayerID!r}, Salary={self.Salary!r}, ContractExpiry={self.ContractExpiry!r}, PlayingStyle={self.PlayingStyle!r}, xTV={self.xTV!r}, PlayerRating={self.PlayerRating!r}, PlayerPotential={self.PlayerPotential!r}, GBEStatus={self.GBEStatus!r}, MinutesPlayed={self.MinutesPlayed!r})"
