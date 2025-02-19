import os
import logging
from urllib.parse import urlencode
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Numeric, event, text, DECIMAL, Decimal, Date
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.sql import func
from datetime import datetime

# ✅ Enable SQLAlchemy Logging
logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

Base = declarative_base()

# ✅ PlayerHistory Model (Stores old player records)
class PlayerMetrics(Base):
    __tablename__ = 'PlayerMetrics'

    MetricsID = Column(Integer, primary_key=True,autoincrement= True)
    PlayerID = Column(Integer, ForeignKey('players.PlayerID'))
    Salary = Column(Decimal)
    ContractExpiry = Column(Date)
    PlayingStyle = Column(String(100))
    xTV = Column(Decimal)
    PlayerRating = Column(Decimal)
    PlayerPotential = Column(Decimal)
    GBEStatus = Column(String(100))
    MinutesPlayed = Column(Decimal)

    # Relationships
    player = relationship("Players", back_populates="metrics")



class Players(Base):
    __tablename__ = 'Players'

    PlayerID = Column(Integer, primary_key=True)

    Name = Column(String(100), unique=True)  
    BirthDate = Column(DateTime)
    FirstPosition = Column(String(100))
    Nationality1 = Column(String(100))
    Nationality2 = Column(String(100), nullable=True)
    ParentTeam = Column(String(100))
    Rating = Column(Numeric(3, 1))
    Transfervalue = Column(Numeric(10, 2))
    Competition_id = Column(Integer, ForeignKey('Competition.Competition_id'), nullable=True)
    fk_players_team = Column(Integer, ForeignKey('Teams.Team_id'), nullable=True)

    metrics = relationship("PlayerMetrics", back_populates="player")



class Teams(Base):
    __tablename__ = 'Teams'

    Team_id = Column(Integer, primary_key=True)
    TeamName = Column(String(100), unique=True, nullable=False)

    # Relationships
    players = relationship("Players", back_populates="team", cascade="all, delete-orphan")
    history = relationship("PlayerHistory", back_populates="team", cascade="all, delete-orphan")



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
    request_url = 'https://apiprod.transferroom.com/api/external/players?position=0&amount=10000'
    headers = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.get(request_url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching player data: {e}")
        return []
    

def process_player(player):
    """Process a single player entry and allow NULL for country_id."""
    db = SessionLocal()

    try:
        player_name = player.get("Name")
        player_id = player.get("TR_ID")

        if not player_id:
            print(f"⚠️ Skipping record, no valid TR_ID found: {player}")
            return

        
        competition_name = competition_name.strip()
        parent_team_name = parent_team_name.strip()

        birth_date = datetime.strptime(birth_date, "%Y-%m-%dT%H:%M:%S") if birth_date else None

        existing_player = db.query(Players).filter_by(PlayerID=player_id).first()
        if existing_player:
            print(f"⏩ Skipping existing player: {player_name} (ID: {player_id})")
            re
        # ✅ Insert player, allowing NULL for player_Country_id
        new_player_metrics = Players(
            PlayerID=player_id,
            Name=player_name,
            BirthDate=birth_date,
            FirstPosition=first_position,
            Nationality1=nationality1,
            Nationality2=nationality2,
            ParentTeam=parent_team_name,
            Rating=rating,
            Transfervalue=transfer_value,
            Competition_id=competition_id,
            player_Country_id=country_id,  # ✅ This can now be NULL
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







