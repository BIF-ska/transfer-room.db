from sqlalchemy import Column, Integer, String, create_engine, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import pycountry
import os

Base = declarative_base()


class PlayersInfo(Base):
    __tablename__ = "PlayersInfo"

    PlayersInfoID = Column(Integer, primary_key=True, autoincrement=True)
    TransferID = Column(Integer, ForeignKey('TransferInfo.TransferID'), nullable=False)
    PlayerID = Column(Integer, ForeignKey('Players.PlayerID'), nullable=False)
    Rating = Column(Integer, nullable=True)  # assuming rating is a number

    # Relationships
    transfer_info = relationship("TransferInfo", back_populates="players_info")
    player = relationship("Players", back_populates="players_info")

    def __repr__(self):
        return f"PlayersInfo(PlayersInfoID={self.PlayersInfoID!r}, TransferID={self.TransferID!r}, PlayerID={self.PlayerID!r}, Rating={self.Rating!r})"