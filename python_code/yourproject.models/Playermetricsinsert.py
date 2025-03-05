import json
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv
from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Players(Base):
    __tablename__ = 'Players'

    PlayerID = Column(Integer, primary_key=True)
    TR_ID = Column(Integer, unique=True)  # Ensure TR_ID exists
    Name = Column(String(100))
    BirthDate = Column(Date)
    FirstPosition = Column(String(100))
    Nationality1 = Column(String(100))
    Nationality2 = Column(String(100), nullable=True)
    ParentTeam = Column(String(100))
    Rating = Column(Numeric(3, 1))
    Transfervalue = Column(Numeric(10, 2))
    Competition_id = Column(Integer, ForeignKey('Competition.Competition_id'))
    fk_players_team = Column(Integer, ForeignKey('Teams.Team_id'))

    metrics = relationship("PlayerMetrics", back_populates="player")


class PlayerMetrics(Base):
    __tablename__ = 'PlayerMetrics'

    MetricsID = Column(Integer, primary_key=True, autoincrement=True)
    PlayerID = Column(Integer, ForeignKey('Players.PlayerID'), nullable=False)
    Salary = Column(Numeric(18, 0), nullable=True)
    ContractExpiry = Column(Date, nullable=True)
    PlayingStyle = Column(String(100), nullable=True)
    xTV = Column(Numeric(18, 0), nullable=True)
    PlayerRating = Column(Numeric(18, 0), nullable=True)
    PlayerPotential = Column(Numeric(18, 0), nullable=True)
    GBResult = Column(String(100), nullable=True)
    MinutesPlayed = Column(Numeric(18, 0), nullable=True)
    GBEScore = Column(Integer, nullable=True)
    BaseValue = Column(Numeric(18, 0), nullable=True)
    EstimatedSalary = Column(String, nullable=True)

    player = relationship("Players", back_populates="metrics")


# Load environment variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Database connection
engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# JSON file path
json_file = r"C:\Users\ska\OneDrive - Brøndbyernes IF Fodbold\Dokumenter\GitHub\transfer-room.db\excels\players_487.json"

# Open a database session
session = SessionLocal()

try:
    # Load JSON data
    with open(json_file, "r", encoding="utf-8") as f:
        player_metrics_data = json.load(f)

    metrics_entries = []

    # Get all players from competition 487
    eligible_players = session.query(Players).filter(Players.Competition_id == 487).all()
    
    # Create a mapping: TR_ID → PlayerID
    tr_id_to_player_id = {player.TR_ID: player.PlayerID for player in eligible_players if player.TR_ID}

    for entry in player_metrics_data:
        tr_id = entry.get("TR_ID")  # Get TR_ID from JSON
        if not tr_id or tr_id not in tr_id_to_player_id:
            print(f"Skipping entry, no matching PlayerID found for TR_ID {tr_id}")
            continue  # Skip if TR_ID is missing or doesn't exist in our DB mapping

        # Create a PlayerMetrics instance with the correct PlayerID
        metrics = PlayerMetrics(
            PlayerID=tr_id_to_player_id[tr_id],  # Get PlayerID from mapping
            Salary=entry.get("Salary"),
            ContractExpiry=entry.get("ContractExpiry"),
            PlayingStyle=entry.get("PlayingStyle"),
            xTV=entry.get("xTV"),
            PlayerRating=entry.get("PlayerRating"),
            PlayerPotential=entry.get("PlayerPotential"),
            GBResult=entry.get("GBResult"),
            MinutesPlayed=entry.get("MinutesPlayed"),
            GBEScore=entry.get("GBEScore"),
            BaseValue=entry.get("BaseValue"),
            EstimatedSalary=entry.get("EstimatedSalary")
        )
        metrics_entries.append(metrics)

    # Bulk insert metrics to improve performance
    if metrics_entries:
        session.bulk_save_objects(metrics_entries)
        session.commit()
        print(f"Inserted {len(metrics_entries)} player metrics successfully!")
    else:
        print("No valid player metrics found in the JSON file.")

except Exception as e:
    session.rollback()
    print(f"Error inserting player metrics: {e}")
finally:
    session.close()
