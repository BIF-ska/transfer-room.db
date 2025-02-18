from sqlalchemy import Column, Integer, String, create_engine, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import pycountry
import os

Base = declarative_base()


class TransferInfo(Base):
    __tablename__ = "TransferInfo"

    TransferID = Column(Integer, primary_key=True, autoincrement=True)
    TransferValue = Column(Integer, nullable=False)

    # Relationships
    players_info = relationship("PlayersInfo", back_populates="transfer_info")

    def __repr__(self):
        return f"TransferInfo(TransferID={self.TransferID!r}, TransferValue={self.TransferValue!r})"