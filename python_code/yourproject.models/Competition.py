from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

columns_dict = {
    "Competition_id": Column(Integer, primary_key=True),
    "Competitionname": Column(String(100)),
    "divisionLevel" : Column(Integer) , 
    }

class Competition(Base):
    __tablename__ = "Competition"
    
    Competition_id = Column(Integer, primary_key=True)
    Competitionname = Column(String(100))
    divisionLevel = Column(Integer) 
    Country_id = Column(Integer, ForeignKey('Country.Country_id'))
    
    #Relationships
    country = relationship('Country', back_populates='competitions')
    #teams = relationship("Teams", back_populates="competition")

    def __repr__(self):
        return f"Competition(id={self.Competition_id!r}, Competitionname={self.Competitionname!r}, divisionLevel={self.divisionLevel!r}, Country_id={self.Country_id!r})"