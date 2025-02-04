from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, BigInteger
from sqlalchemy.orm import relationship
from datetime import datetime
from models import Base


columns_dict = {
    "Team_id": Column(Integer, primarykey=True),
    "Teamname": Column(String(100)),
    "Competetition_ID": Column(Integer, ForeignKey=True),
    "Country_ID": Column(Integer, ForeignKey=True),
    }

class Teams(Base):
   


    __tablename__ = "teams"
    Team_id = Column(Integer, primarykey=True)
    Teamname = Column(String(100))
    Competetition_ID = Column(Integer, ForeignKey("competetion.id"))
    Country_ID = Column(Integer, ForeignKey("country.id"))

    # Relationships
    player = relationship("Player")
    team = relationship("Team")

    def __repr__(self):
        return f"Teams(Team_id={self.Team_id!r}, Teamname={self.Teamname!r}, Competetition_ID={self.Competetition_ID!r}, Country_ID={self.Country_ID!r})"