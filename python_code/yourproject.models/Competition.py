from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Competition(Base):
    __tablename__ = "Competition"

    Competition_id = Column(Integer, primary_key=True)
    Competitionname = Column(String(100))
    divisionLevel = Column(Integer)
    country_fk_id = Column(Integer, ForeignKey("Country.Country_id"))  # Use string reference to avoid circular import

    # Relationships
# In Competition class
    # In Country class
    country = relationship("Country", back_populates="competitions")



    def __repr__(self):
        return (
            f"Competition(id={self.Competition_id!r}, "
            f"Competitionname={self.Competitionname!r}, "
            f"divisionLevel={self.divisionLevel!r}, "
            f"country_fk_id={self.country_fk_id!r})"
        )  # 🔴 Ensure this method ends properly before defining anything else
