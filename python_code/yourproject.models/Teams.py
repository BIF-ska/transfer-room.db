from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Teams(Base):
    __tablename__ = "Teams"
    
    Team_id = Column(Integer, primary_key=True, autoincrement=True)
    Teamname = Column(String(100))
    Teamrating = Column(DECIMAL(10, 2))
    Competition_id = Column(Integer, ForeignKey("Competition.Competition_id"))
    Country_id = Column(Integer, ForeignKey("Country.Country_id"))
    
    # Relationships
    country = relationship("Country", back_populates="teams")
    competition_team = relationship("Competition", back_populates="teams")
    # players = relationship("Players", back_populates="team")

    def __repr__(self):
        return (f"Teams(Team_id={self.Team_id!r}, Teamname={self.Teamname!r}, "
                f"Competition_id={self.Competition_id!r}, Country_id={self.Country_id!r})")
