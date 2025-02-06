from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

columns_dict = {
    "Team_id": Column(Integer, primary_key=True),
    "Teamname": Column(String(100)),
    "Competition_id": Column(Integer, ForeignKey("Competition.Competition_id")),  # correct reference
    "Country_id": Column(Integer, ForeignKey("Country.Country_id")),
}

class Teams(Base):
    __tablename__ = "Teams"
    
    Team_id = Column(Integer, primary_key=True)
    Teamname = Column(String(100))
    # Instead of ForeignKey=True, provide the "table.column" reference:
    Competition_id = Column(Integer, ForeignKey("Competition.Competition_id"))
    Country_id = Column(Integer, ForeignKey("Country.Country_id"))
    
    # Relationships
    country = relationship("Country", back_populates="teams")
    competition = relationship("Competition", back_populates="teams")
    players = relationship("Players", back_populates="team")

    def __repr__(self):
        return (f"Teams(Team_id={self.Team_id!r}, Teamname={self.Teamname!r}, "
                f"Competition_id={self.Competition_id!r}, Country_id={self.Country_id!r})")
