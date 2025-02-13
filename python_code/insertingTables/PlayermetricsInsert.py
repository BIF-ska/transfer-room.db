import os
from datetime import datetime
import requests
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, Numeric, DECIMAL
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

class Players(Base):
    __tablename__ = 'Players'

    PlayerID = Column(Integer, primary_key=True)
    Name = Column(String(100))
    BirthDate = Column(Date)
    FirstPosition = Column(String(100))
    Nationality1 = Column(String(100))
    Nationality2 = Column(String(100), nullable=True)
    ParentTeam = Column(String(100))
    Rating = Column(Numeric(3, 1))
    Transfervalue = Column(Numeric(10, 2))

    # Relationships
    metrics = relationship("PlayerMetrics", back_populates="player")

class PlayerMetrics(Base):
    __tablename__ = 'PlayerMetrics'

    MetricsID = Column(Integer, primary_key=True)
    PlayerID = Column(Integer, ForeignKey('Players.PlayerID'))
    Salary = Column(DECIMAL)
    ContractExpiry = Column(Date)
    PlayingStyle = Column(String(100))
    xTV = Column(DECIMAL)
    PlayerRating = Column(DECIMAL)
    PlayerPotential = Column(DECIMAL)
    GBEStatus = Column(String(100))
    MinutesPlayed = Column(DECIMAL)

    # Relationships
    player = relationship("Players", back_populates="metrics")

def safe_numeric(value):
    """Convert valid numbers; replace invalid ones with None (NULL in SQL)"""
    if isinstance(value, (int, float)):  # Check if it's already a valid number
        return value
    try:
        return float(value)  # Try to convert if it's a valid numeric string
    except (ValueError, TypeError):
        return None  # If conversion fails, return None

def seed_player_metrics():
    load_dotenv()
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("No DATABASE_URL found.")
        return

    engine = create_engine(db_url, echo=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    email = os.getenv("email")
    password = os.getenv("password")
    base_url = os.getenv("base_url")
    params = {'email': email, 'password': password}

    try:
        r = requests.post(auth_url, params=params)
        r.raise_for_status()
        token = r.json().get('token')
        if not token:
            raise ValueError("Token not found in the API response.")
    except requests.exceptions.RequestException as e:
        print(f"Error during authentication: {e}")
        return
    except ValueError as e:
        print(f"Error parsing token: {e}")
        return

    headers = {"Authorization": f"Bearer {token}"}

    request_url = 'https://apiprod.transferroom.com/api/external/players'
    try:
        r = requests.get(request_url, headers=headers)
        r.raise_for_status()
        players_data = r.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching player data: {e}")
        return

    for player in players_data:
        try:
            # Extract player name & TR_ID
            player_name = player.get("Name")
            tr_id = player.get("TR_ID")

            # DEBUG: Print to verify API data
            print(f"Processing Player: Name={player_name}, TR_ID={tr_id}")

            # ✅ Find the player in DB by Name (since TR_ID may not match PlayerID)
            existing_player = db.query(Players).filter(Players.Name.ilike(player_name)).first()
            if not existing_player:
                print(f"⚠️ Skipping player {player_name}: Not found in Players table.")
                continue  # Skip inserting metrics for non-existing players

            player_id = existing_player.PlayerID

            # ✅ Check if metrics already exist for the player
            existing_metrics = db.query(PlayerMetrics).filter_by(PlayerID=player_id).first()
            if existing_metrics:
                print(f"✅ Metrics already exist for player {player_name}, skipping.")
                continue  # Skip if metrics already exist

            # ✅ Extract player metrics with safe conversion
            salary = safe_numeric(player.get('EstimatedSalary'))
            contract_expiry = player.get('ContractExpiry')
            playing_style = player.get('PlayingStyle') if player.get('PlayingStyle') != "UPGRADE TO ACCESS" else None
            xtv = safe_numeric(player.get('xTV'))
            player_rating = safe_numeric(player.get('Rating'))
            player_potential = safe_numeric(player.get('Potential'))
            gbe_status = player.get('GBEResult') if player.get('GBEResult') != "UPGRADE TO ACCESS" else None
            minutes_played = safe_numeric(player.get('CurrentClubRecentMinsPerc'))

            # ✅ Convert contract expiry date safely
            contract_expiry_date = None
            if contract_expiry and contract_expiry != "UPGRADE TO ACCESS":
                try:
                    contract_expiry_date = datetime.strptime(contract_expiry, '%Y-%m-%dT%H:%M:%S').date()
                except ValueError:
                    print(f"⚠️ Invalid date format for player {player_name}: {contract_expiry}. Setting as NULL.")
                    contract_expiry_date = None  # Instead of skipping, store as NULL

            # ✅ Insert new player metrics
            new_metrics = PlayerMetrics(
                PlayerID=player_id,  # ✅ Using matched PlayerID
                Salary=salary,
                ContractExpiry=contract_expiry_date,
                PlayingStyle=playing_style,
                xTV=xtv,
                PlayerRating=player_rating,
                PlayerPotential=player_potential,
                GBEStatus=gbe_status,
                MinutesPlayed=minutes_played
            )
            db.add(new_metrics)
            db.commit()

            print(f"✅ Added metrics for player {player_name} (PlayerID: {player_id}).")

        except Exception as e:
            db.rollback()
            print(f"❌ Error processing player {player_name}: {e}")

    db.close()

if __name__ == "__main__":
    seed_player_metrics()
