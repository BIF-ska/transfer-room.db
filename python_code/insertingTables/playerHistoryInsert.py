import os
import json
import logging
from urllib.parse import urlencode
from datetime import datetime
import requests
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Numeric, event
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.sql import func
from playerinsert import Country, Competition, Teams, Players

# ✅ Enable SQLAlchemy Logging to See Queries in Console
logging.basicConfig(level=logging.INFO, force=True)

Base = declarative_base()

# ✅ PlayerHistory Model (Stores old player records)
class Country(Base):
    __tablename__ = 'Country'
    
    Country_id = Column(Integer, primary_key=True)
    Name = Column(String(100), nullable=False)
    
    competitions = relationship("Competition", back_populates="country")
    teams = relationship("Teams", back_populates="country")

class Competition(Base):
    __tablename__ = 'Competition'

    Competition_id = Column(Integer, primary_key=True)
    Competitionname = Column(String(100), nullable=False)
    divisionLevel = Column(Integer, nullable=False)
    country_fk_id = Column(Integer, ForeignKey("Country.Country_id"))
    
    country = relationship("Country", back_populates="competitions")
    teams = relationship("Teams", back_populates="competition_team")

class Teams(Base):
    __tablename__ = "Teams"

    Team_id = Column(Integer, primary_key=True, autoincrement=True)
    Teamname = Column(String(100), unique=True)
    Competition_id = Column(Integer, ForeignKey("Competition.Competition_id"))
    Country_id = Column(Integer, ForeignKey("Country.Country_id"))
    
    country = relationship("Country", back_populates="teams")
    competition_team = relationship("Competition", back_populates="teams")
    players = relationship("Players", back_populates="team")
    history = relationship("PlayerHistory", back_populates="team", cascade="all, delete-orphan")


class PlayerHistory(Base):
    __tablename__ = "PlayerHistory"
    
    HistoryID = Column(Integer, primary_key=True, autoincrement=True)
    PlayerID = Column(Integer, ForeignKey("Players.PlayerID", ondelete="CASCADE"), nullable=False)
    TeamID = Column(Integer, ForeignKey("Teams.Team_id", ondelete="CASCADE"), nullable=False)
    Name = Column(String(100), nullable=False)
    Rating = Column(Numeric(3, 1), nullable=True)
    Transfervalue = Column(Numeric(10, 2), nullable=True)
    UpdatedAt = Column(DateTime, server_default=func.now(), nullable=False)

    # Relationships
    player = relationship("Players", back_populates="history")
    team = relationship("Teams", back_populates="history")


# ✅ Players Model
class Players(Base):
    __tablename__ = 'Players'

    PlayerID = Column(Integer, primary_key=True)
    Name = Column(String(100), unique=True)  # Prevent duplicate player names
    BirthDate = Column(DateTime)
    FirstPosition = Column(String(100))
    Nationality1 = Column(String(100))
    Nationality2 = Column(String(100), nullable=True)
    ParentTeam = Column(String(100))
    Rating = Column(Numeric(3, 1))
    Transfervalue = Column(Numeric(10, 2))
    Competition_id = Column(Integer, ForeignKey('Competition.Competition_id'), nullable=True)
    fk_players_team = Column(Integer, ForeignKey('Teams.Team_id'), nullable=True)

    # Relationships
    team = relationship("Teams", back_populates="players")
    history = relationship("PlayerHistory", back_populates="player", cascade="all, delete-orphan")





# ✅ Load environment variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# ✅ Create database engine & session
engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# ✅ Function to Fetch API Token
def fetch_api_token():
    """Fetch API authentication token."""
    email = os.getenv("email")
    password = os.getenv("password")
    base_url = os.getenv("base_url")
    auth_url = f"{base_url}?{urlencode({'email': email, 'password': password})}"

    try:
        response = requests.post(auth_url)
        response.raise_for_status()
        token_data = response.json()
        print("✅ Successfully authenticated.")
        return token_data.get("token")
    
    except requests.RequestException as e:
        print(f"Error during authentication: {e}")
        return None


# ✅ Function to Fetch Players Data
def fetch_players_data_and_update(token):
    """
    Fetch player data from API and automatically update database if there are changes.
    """
    request_url = 'https://apiprod.transferroom.com/api/external/players'
    headers = {"Authorization": f"Bearer {token}"}

    session = SessionLocal()

    try:
        response = requests.get(request_url, headers=headers)
        response.raise_for_status()
        json_data = response.json()

        if not isinstance(json_data, list):
            print("❌ Unexpected API response format.")
            return

        print("✅ API Data Fetched Successfully!")

        for player_data in json_data:
            player_id = player_data.get("PlayerID")
            new_transfer_value = player_data.get("Transfervalue")

            # Fetch existing player record
            player = session.query(Players).filter(Players.PlayerID == player_id).first()

            if player:
                # ✅ Only update if transfer value changed
                if player.Transfervalue != new_transfer_value:
                    print(f"🔄 Updating {player.Name}'s transfer value from {player.Transfervalue} to {new_transfer_value}")

                    # Save old value in PlayerHistory
                    history_record = PlayerHistory(
                        PlayerID=player.PlayerID,
                        TeamID=player.fk_players_team,
                        Name=player.Name,
                        Rating=player.Rating,
                        Transfervalue=player.Transfervalue
                    )
                    session.add(history_record)

                    # Update player transfer value
                    player.Transfervalue = new_transfer_value
                    session.commit()
                    print(f"✅ Updated {player.Name}'s transfer value.")
                else:
                    print(f"⚠️ No changes for {player.Name}. Skipping update.")
            else:
                print(f"⚠️ Player ID {player_id} not found in database. Skipping.")

    except requests.RequestException as e:
        print(f"❌ Error fetching player data: {e}")

    finally:
        session.close()



if __name__ == "__main__":
    token = fetch_api_token()
    if token:
        fetch_players_data_and_update(token)  # ✅ Automatically update players