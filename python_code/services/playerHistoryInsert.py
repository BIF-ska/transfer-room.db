import datetime
import json
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, exists
from dotenv import load_dotenv
from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
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

    history = relationship("PlayerHistory", back_populates="player")


class PlayerHistory(Base):
    __tablename__ = "PlayerHistory"

    HistoryID = Column(Integer, primary_key=True, autoincrement=True)
    PlayerID = Column(Integer, ForeignKey("Players.PlayerID"), nullable=False)
    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    xTV = Column(Numeric(18, 2), nullable=False)
    UpdatedAt = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    Name= Column(String(100), nullable=False)

    # Relationship with Players Table
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
    json_file = r"C:\\Users\\ska\\OneDrive - Brøndbyernes IF Fodbold\\Dokumenter\\GitHub\\transfer-room.db\\excels\\players_487.json"

    with open(json_file, "r", encoding="utf-8") as f:
        player_data = json.load(f)

    # 🔥 Step 4: Process Each Player Entry
    for player_entry in player_data:
        tr_id = player_entry.get("TR_ID")
        if not tr_id or tr_id not in tr_id_to_player:
            print(f"Skipping player, no matching PlayerID found for TR_ID {tr_id}")
            continue  # Skip players not in our competition

        player_id, player_name = tr_id_to_player[tr_id]  # Get PlayerID & Name from mapping

        # 🔥 Step 5: Extract xTVHistory JSON (It's a string, so convert it)
        xtv_history_raw = player_entry.get("xTVHistory")
        if not xtv_history_raw:
            continue  # Skip if no xTdV history

        xtv_history = json.loads(xtv_history_raw)  # Convert JSON string to a list of dicts

        # 🔥 Step 6: Insert Each xTV History Entry into PlayerHistory Table
        for history_entry in xtv_history:
            new_history = PlayerHistory(
                PlayerID=player_id,
                year=history_entry["year"],
                month=history_entry["month"],
                xTV=history_entry["xTV"],
                UpdatedAt=datetime.datetime.utcnow(),
                Name=player_name  # ✅ Now using the correct player name!

            )
            session.add(new_history)

    # 🔥 Commit all transactions
    session.commit()
    print("✅ Successfully inserted xTV history into PlayerHistory table!")

except Exception as e:
    session.rollback()
    print(f"❌ Error: {e}")
finally:
    session.close()
