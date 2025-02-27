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
from datetime import datetime, timezone

from sqlalchemy.orm import Session
from sqlalchemy import event



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
    PlayerID = Column(Integer, ForeignKey("Players.PlayerID", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    TeamID = Column(Integer, ForeignKey("Teams.Team_id", ondelete="CASCADE"), nullable=False)
    Name = Column(String(100), nullable=False)
    Rating = Column(Numeric(3, 1), nullable=True)
    Transfervalue = Column(Numeric(10, 2), nullable=True)
    UpdatedAt = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    # ✅ FIXED: Removed delete-orphan (only keep back_populates)
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
    TR_ID = Column(Integer, nullable=False)

    # Relationships
    team = relationship("Teams", back_populates="players")
    history = relationship("PlayerHistory", back_populates="player", cascade="all, delete-orphan")



@event.listens_for(Session, "before_flush")
def update_player_history(session, flush_context, instances):
    """
    Automatically update PlayerHistory when a player's TR_ID (PlayerID) changes.
    """
    for instance in session.dirty:  # Checks modified records
        if isinstance(instance, Players):
            session.query(PlayerHistory).filter(
                PlayerHistory.PlayerID == instance.PlayerID
            ).update({PlayerHistory.PlayerID: instance.PlayerID})





# ✅ Load environment variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# ✅ Create database engine & session
engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



# ✅ Function to Fetch Players Data
# ✅ Function to Fetch Players Data from JSON File Instead of API
def fetch_players_data_and_update():
    """
    Fetch player data from a local JSON file and update database if there are changes.
    """
    file_path = r"C:\Users\ska\OneDrive - Brøndbyernes IF Fodbold\Dokumenter\GitHub\transfer-room.db\players_data.json"

    session = SessionLocal()

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            json_data = json.load(file)

        if not isinstance(json_data, list):
            print("❌ Unexpected file format. Expected a list of players.")
            return

        print("✅ Player data loaded from JSON successfully!")

        for player_data in json_data:
            tr_id = player_data.get("TR_ID")  # ✅ Use TR_ID instead of PlayerID
            new_transfer_value = player_data.get("xTV")  # ✅ Use xTV for transfer value
            new_team_name = player_data.get("CurrentTeam")  # ✅ Use CurrentTeam

            # Fetch existing player record using TR_ID
            player = session.query(Players).filter(Players.TR_ID == tr_id).first()

            if player:
                update_required = False

                # ✅ Ensure team exists in Teams table
                new_team = session.query(Teams).filter(Teams.Teamname == new_team_name).first()
                new_team_id = new_team.Team_id if new_team else None  # Get the ID if found

                # ✅ Track transfer value change
                if player.Transfervalue != new_transfer_value:
                    print(f"🔄 Updating {player.Name}'s transfer value from {player.Transfervalue} to {new_transfer_value}")
                    update_required = True

                # ✅ Track team change
                if player.fk_players_team != new_team_id:
                    print(f"🔄 {player.Name} has changed teams from {player.fk_players_team} to {new_team_id}")
                    update_required = True

                if update_required:
                    # Save old values in PlayerHistory before modifying Players table
                    history_record = PlayerHistory(
                        PlayerID=player.TR_ID,  # ✅ Use TR_ID instead of PlayerID
                        TeamID=player.fk_players_team,  # Save previous team ID
                        Name=player.Name,
                        Rating=player.Rating,
                        Transfervalue=player.Transfervalue,  # Save previous transfer value
                        UpdatedAt=datetime.utcnow()  # Ensure timestamp is correct
                    )
                    session.add(history_record)

                    # Update player data
                    player.Transfervalue = new_transfer_value
                    player.fk_players_team = new_team_id  # Update team
                    session.commit()
                    print(f"✅ Updated {player.Name}'s details.")

                else:
                    print(f"⚠️ No changes for {player.Name}. Skipping update.")
            else:
                print(f"⚠️ Player TR_ID {tr_id} not found in database. Skipping.")

    except FileNotFoundError:
        print(f"❌ Error: The file {file_path} was not found.")
    except json.JSONDecodeError:
        print("❌ Error: Failed to decode JSON. Check file format.")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    finally:
        session.close()



if __name__ == "__main__":
    fetch_players_data_and_update()