import json
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, exists
from dotenv import load_dotenv
from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey, DateTime
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Players(Base):
    __tablename__ = 'Players'
 
    PlayerID = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(100), unique=True)
    BirthDate = Column(DateTime)
    FirstPosition = Column(String(100))
    Nationality1 = Column(String(100))
    Nationality2 = Column(String(100), nullable=True)
    ParentTeam = Column(String(100))
    Rating = Column(Numeric(3, 1))
    Transfervalue = Column(Numeric(10, 2))
    Competition_id = Column(Integer, ForeignKey('Competition.Competition_id'), nullable=False)
    player_Country_id = Column(Integer, ForeignKey('Country.Country_id'), nullable=True)
    TR_ID = Column(Integer, nullable=False)
    fk_players_team = Column(Integer, ForeignKey('Teams.Team_id'), nullable=True)

    history = relationship("TeamHistory", back_populates="player")

# Define Team_History Table
class TeamHistory(Base):
    __tablename__ = 'Team_History'

    history_id = Column(Integer, primary_key=True, autoincrement=True)
    player_id = Column(Integer, ForeignKey('Players.PlayerID'), nullable=False)
    from_team = Column(String(255), nullable=False)  # Store team name instead of ID
    to_team = Column(String(255), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)  # Nullable if empty
    transfer_type = Column(String(50), nullable=False)
    transfer_fee_euros = Column(Numeric(18, 2), nullable=False, default=0)
    created_at = Column(Date, server_default="GETDATE()", nullable=False)
    name = Column(String(100), nullable=False)  # Player Name

    player = relationship("Players", back_populates="history")

# Load environment variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Database connection
engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Open a database session
session = SessionLocal()

try:
    # 🔥 Step 1: Get Eligible Players (Only for Competition 487)
    eligible_players = session.query(Players).filter(Players.Competition_id == 487).all()

    # 🔥 Step 2: Create Mapping TR_ID → PlayerID + Player Name
    tr_id_to_player = {player.TR_ID: (player.PlayerID, player.Name) for player in eligible_players if player.TR_ID}

    # 🔥 Step 3: Load JSON File
    json_file = r"C:\Users\ska\OneDrive - Brøndbyernes IF Fodbold\Dokumenter\GitHub\transfer-room.db\excels\players_487.json"

    with open(json_file, "r", encoding="utf-8") as f:
        player_data = json.load(f)

    # 🔥 Step 4: Loop Through Each Player's Data
    for player_entry in player_data:
        tr_id = player_entry.get("TR_ID")
        if not tr_id or tr_id not in tr_id_to_player:
            print(f"Skipping player, no matching PlayerID found for TR_ID {tr_id}")
            continue  # Skip players not in our competition

        player_id, player_name = tr_id_to_player[tr_id]  # Get PlayerID & Name from mapping

        # 🔥 Step 5: Extract `TeamHistory` JSON (It's a string, so convert it)
        team_history_raw = player_entry.get("TeamHistory")
        if not team_history_raw:
            continue  # Skip if no transfer history

        try:
            team_history_entries = json.loads(team_history_raw)  # Convert string to JSON list
        except json.JSONDecodeError as e:
            print(f"Error decoding TeamHistory JSON for TR_ID {tr_id}: {e}")
            continue  # Skip if JSON is invalid

        # 🔥 Step 6: Insert Each Transfer as a Separate Row
        for entry in team_history_entries:
            from_team = entry.get("FromTeam")
            to_team = entry.get("ToTeam")
            start_date = entry.get("StartDate")
            end_date = entry.get("EndDate") if entry.get("EndDate") else None
            transfer_type = entry.get("TransferType")
            transfer_fee = float(entry.get("TransferFeeEuros"))

            # 🚀 **Check for Existing Transfer to Prevent Duplicates**
            existing_transfer = session.query(TeamHistory).filter_by(
                player_id=player_id,
                from_team=from_team,
                to_team=to_team,
                start_date=start_date
            ).first()

            if existing_transfer:
                print(f"Skipping duplicate transfer: {entry}")
                continue

            # 🚀 **Insert New Transfer with Player Name**
            transfer = TeamHistory(
                player_id=player_id,
                from_team=from_team,
                to_team=to_team,
                start_date=start_date,
                end_date=end_date,
                transfer_type=transfer_type,
                transfer_fee_euros=transfer_fee,
                name=player_name  # ✅ Now using the correct player name!
            )

            session.add(transfer)

    # 🔥 Step 7: Commit to Database
    session.commit()
    print("Inserted all team history records successfully!")

except Exception as e:
    session.rollback()
    print(f"Error inserting team history: {e}")

finally:
    session.close()
