import os
import json
import threading
from urllib.parse import urlencode
from datetime import datetime
import requests
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Numeric
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

# Database models
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

    team = relationship("Teams", back_populates="players")


# Load environment variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Create a database engine
engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20, echo=False)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


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
        return token_data.get("token")
    except requests.RequestException as e:
        print(f"Error during authentication: {e}")
        return None


def fetch_players_data(token):
    """Fetch player data from API."""
    request_url = 'https://apiprod.transferroom.com/api/external/players'
    headers = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.get(request_url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching player data: {e}")
        return []


def process_player(player):
    """Process a single player entry in a separate thread-safe session."""
    db = SessionLocal()

    try:
        player_name = player.get("Name")
        player_id = player.get("TR_ID")  # ✅ Use TR_ID as PlayerID

        if not player_id:
            print(f"⚠️ Skipping record, no valid TR_ID found: {player}")
            return

        birth_date = player.get("BirthDate")
        first_position = player.get("FirstPosition")
        nationality1 = player.get("Nationality1")
        nationality2 = player.get("Nationality2")
        parent_team_name = player.get("CurrentTeam") or "Unknown Team"
        competition_name = player.get("Competition") or "Unknown Competition"
        rating = player.get("Rating")
        transfer_value = player.get("xTV")

        # ✅ Ensure strings are valid
        competition_name = competition_name.strip()
        parent_team_name = parent_team_name.strip()

        # ✅ Convert birth date if available
        birth_date = datetime.strptime(birth_date, "%Y-%m-%dT%H:%M:%S") if birth_date else None

        # ✅ Check if player already exists by TR_ID
        existing_player = db.query(Players).filter_by(PlayerID=player_id).first()

        if existing_player:
            print(f"⏩ Skipping existing player: {player_name} (ID: {player_id})")
            return

        # ✅ Ensure competition exists or create it
        competition = db.query(Competition).filter_by(Competitionname=competition_name).first()
        if not competition:
            print(f"⚠️ Creating new competition: {competition_name}")
            competition = Competition(Competitionname=competition_name, divisionLevel=1)
            db.add(competition)
            db.commit()
            db.refresh(competition)

        competition_id = competition.Competition_id

        # ✅ Ensure team exists or create it
        team = db.query(Teams).filter_by(Teamname=parent_team_name).first()
        if not team:
            print(f"⚠️ Creating new team: {parent_team_name}")
            team = Teams(Teamname=parent_team_name, Competition_id=competition_id)
            db.add(team)
            db.commit()
            db.refresh(team)

        team_id = team.Team_id

        print(f"✅ Inserting player {player_name} -> Team ID: {team_id}, Competition ID: {competition_id}")

        # ✅ Insert the player with correct PlayerID (TR_ID)
        new_player = Players(
            PlayerID=player_id,  # ✅ Save TR_ID as PlayerID
            Name=player_name,
            BirthDate=birth_date,
            FirstPosition=first_position,
            Nationality1=nationality1,
            Nationality2=nationality2,
            ParentTeam=parent_team_name,
            Rating=rating,
            Transfervalue=transfer_value,
            Competition_id=competition_id,
            fk_players_team=team_id,
        )

        db.add(new_player)
        db.commit()
        print(f"✅ Successfully inserted: {player_name} (ID: {player_id})")

    except Exception as e:
        db.rollback()
        print(f"❌ Error inserting player {player_name}: {e}")

    finally:
        db.close()


def seed_players():
    """Fetch players from API and insert them using threads."""
    token = fetch_api_token()
    if not token:
        print("❌ Failed to authenticate.")
        return

    players_data = fetch_players_data(token)
    if not players_data:
        print("❌ No player data retrieved.")
        return
    print(f"🚀 Processing {len(players_data)} players using threads...")

    print(f"🚀 Processing {len(players_data)} players using threads...")

    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_player = {executor.submit(process_player, player): player for player in players_data}

        for future in as_completed(future_to_player):
            future.result()  # Handle exceptions within threads

    print("🎉 All players processed!")


if __name__ == "__main__":
    seed_players()  # ✅ Correct function call
