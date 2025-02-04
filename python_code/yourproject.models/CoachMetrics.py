from sqlalchemy import Column, Integer, VARCHAR, Boolean, ForeignKey
from decimal import Decimal
from sqlalchemy.orm import relationship
from models import Base

# Defining the columns dictionary for the CoachMetrics model
columns_dict_coach_metrics = {
    "MetricID": Column(Integer, primary_key=True, autoincrement=True),
    "CoachID": Column(Integer, ForeignKey('HeadCoach.CoachID')),
    "Rating": Column(Decimal),
    "TacticalStyle": Column(VARCHAR(100)),
    "RatingChange12M": Column(Decimal),
    "Suitability": Column(Decimal),
    "TeamRatingImpact": Column(Decimal),
    "TrustInYouth": Column(Decimal),
    "PreferredFormation": Column(VARCHAR(100)),
    "SquadRotation": Column(Decimal),
    "AvgTransferSpend": Column(Decimal)
}

# Defining the CoachMetrics model
class CoachMetrics(Base):
    __tablename__ = 'CoachMetrics'

    MetricID = Column(Integer, primary_key=True, autoincrement=True)
    CoachID = Column(Integer, ForeignKey('HeadCoach.CoachID'))
    Rating = Column(Decimal)
    TacticalStyle = Column(VARCHAR(100))
    RatingChange12M = Column(Decimal)
    Suitability = Column(Decimal)
    TeamRatingImpact = Column(Decimal)
    TrustInYouth = Column(Decimal)
    PreferredFormation = Column(VARCHAR(100))
    SquadRotation = Column(Decimal)
    AvgTransferSpend = Column(Decimal)

    # Relationship with the HeadCoach model
    coach = relationship("HeadCoach", back_populates="metrics")

    def __repr__(self):
        return f"CoachMetrics(MetricID={self.MetricID!r}, CoachID={self.CoachID!r}, Rating={self.Rating!r}, TacticalStyle={self.TacticalStyle!r}, RatingChange12M={self.RatingChange12M!r}, Suitability={self.Suitability!r}, TeamRatingImpact={self.TeamRatingImpact!r}, TrustInYouth={self.TrustInYouth!r}, PreferredFormation={self.PreferredFormation!r}, SquadRotation={self.SquadRotation!r}, AvgTransferSpend={self.AvgTransferSpend!r})"
