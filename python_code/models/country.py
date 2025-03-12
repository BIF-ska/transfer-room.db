from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base



# Define your model directly here
class country(Base):
    __tablename__ = "country"

    country_id = Column(Integer, primary_key=True, autoincrement=True)
    country_name = Column(String(255))

    # Relationships
    #competitions = relationship("competition", back_populates="country")




