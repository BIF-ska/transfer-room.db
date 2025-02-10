from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import pycountry
import os

Base = declarative_base()

# Define your model directly here
class Country(Base):
    __tablename__ = "Country"

    Country_id = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(255))

    # Relationships
    competitions = relationship("Competition", back_populates="country")
    teams = relationship("Teams", back_populates="country")


    def __repr__(self):
        return f"Country(Country_id={self.Country_id!r}, Name={self.Name!r})"
