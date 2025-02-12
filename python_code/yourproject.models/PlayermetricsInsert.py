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

def seed_player_metrics():
    load_dotenv()
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("No DATABASE_URL found.")
        return

    engine = create_engine(db_url, echo=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    email = 'dst@brondby.com'
    password = 'BifAdmin1qazZAQ!TransferRoom'
    auth_url = "https://apiprod.transferroom.com/api/external/login"
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
            # Extract player ID
            tr_id = player.get('TR_ID')

            # Check if player exists in the database
            existing_player = db.query(Players).filter_by(PlayerID=tr_id).first()
            if not existing_player:
                print(f"Skipping player {tr_id}: Not found in Players table.")
                continue  # Skip inserting metrics for non-existing players

            # Check if metrics already exist for the player
            existing_metrics = db.query(PlayerMetrics).filter_by(PlayerID=tr_id).first()
            if existing_metrics:
                print(f"Metrics already exist for player {tr_id}, skipping.")
                continue  # Skip if metrics already exist

            # Extract player metrics
            salary = player.get('EstimatedSalary')
            contract_expiry = player.get('ContractExpiry')
            playing_style = player.get('PlayingStyle')
            xtv = player.get('xTV')
            player_rating = player.get('Rating')
            player_potential = player.get('Potential')
            gbe_status = player.get('GBEResult')
            minutes_played = player.get('CurrentClubRecentMinsPerc')

            # Insert new player metrics
            new_metrics = PlayerMetrics(
                PlayerID=tr_id,
                Salary=salary,
                ContractExpiry=datetime.strptime(contract_expiry, '%Y-%m-%dT%H:%M:%S').date() if contract_expiry else None,
                PlayingStyle=playing_style,
                xTV=xtv,
                PlayerRating=player_rating,
                PlayerPotential=player_potential,
                GBEStatus=gbe_status,
                MinutesPlayed=minutes_played
            )
            db.add(new_metrics)
            db.commit()

            print(f"Added metrics for player {tr_id}.")

        except Exception as e:
            print(f"Error processing player {tr_id}: {e}")
            db.rollback()

if __name__ == "__main__":
    seed_player_metrics()
