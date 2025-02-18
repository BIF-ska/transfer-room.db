import os
import logging
from urllib.parse import urlencode
from datetime import datetime
import requests
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Numeric, event, text
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.sql import func

# ✅ Enable SQLAlchemy Logging
logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

Base = declarative_base()

# ✅ PlayerHistory Model (Stores old player records)
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

    # Relationships
    team = relationship("Teams", back_populates="players")
    history = relationship("PlayerHistory", back_populates="player", cascade="all, delete-orphan")


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

# ✅ Check if database URL is loaded
if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL is missing! Check your .env file.")

# Create a database engine
engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20, echo=True)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# ✅ Automatically archive old player records before updates
def before_update_listener(mapper, connection, target):
    """Automatically archive player history before any update."""
    session = SessionLocal()
    
    print(f"📌 Saving old record for {target.Name} (ID: {target.PlayerID}) before update...")

    history_record = PlayerHistory(
        PlayerID=target.PlayerID,
        TeamID=target.fk_players_team,
        Name=target.Name,
        Rating=target.Rating,
        Transfervalue=target.Transfervalue,  
        UpdatedAt=datetime.utcnow()
    )
    
    session.add(history_record)
    session.commit()
    session.close()

    print(f"✅ Archived {target.Name} (ID: {target.PlayerID}) in PlayerHistory.")


# Attach the event listener to track changes in Players
event.listen(Players, "before_update", before_update_listener)


# ✅ Function to fetch all players
def fetch_all_players():
    """Fetch all players from the database."""
    with SessionLocal() as db_session:
        players = db_session.query(Players).all()
        if players:
            print("\n📋 Existing Players in Database:")
            for player in players:
                print(f"ID: {player.PlayerID}, Name: {player.Name}, Rating: {player.Rating}, CTV: {player.Transfervalue}")
        else:
            print("\n❌ No players found in the database.")


# ✅ Function to insert a test player (if missing)
def insert_test_player():
    """Insert a test player if none exists."""
    with SessionLocal() as db_session:
        existing_player = db_session.query(Players).filter(Players.PlayerID == 1).first()
        
        if not existing_player:
            print("🆕 Inserting a test player (ID=1)...")
            new_player = Players(
                PlayerID=1, 
                Name="Messi", 
                BirthDate=datetime(1987, 6, 24), 
                FirstPosition="Forward", 
                Nationality1="Argentina", 
                ParentTeam="Barcelona", 
                Rating=93.0, 
                Transfervalue=1000, 
                fk_players_team=1
            )
            db_session.add(new_player)
            db_session.commit()
            print("✅ Test player inserted successfully!")
        else:
            print("✅ Player ID 1 already exists!")


# ✅ Function to manually update a player
def update_player(player_id, new_data):
    """Updates player record and stores the old record in history."""
    with SessionLocal() as db_session:
        player = db_session.query(Players).filter(Players.PlayerID == player_id).first()

        if player:
            print(f"🔄 Updating {player.Name} (ID: {player.PlayerID}) with new data: {new_data}")
            
            for key, value in new_data.items():
                if hasattr(player, key):
                    setattr(player, key, value)

            db_session.commit()
            print(f"✅ Player {player.Name} updated successfully.")
        else:
            print(f"❌ No player found with ID: {player_id}")


# ✅ Function to delete a player while keeping history
def delete_player(player_id):
    """Deletes a player after archiving their record in PlayerHistory."""
    with SessionLocal() as db_session:
        player = db_session.query(Players).filter(Players.PlayerID == player_id).first()

        if player:
            print(f"🗑️ Deleting player {player.Name} (ID: {player.PlayerID})...")

            db_session.delete(player)
            db_session.commit()
            print(f"✅ Player {player.Name} deleted successfully.")
        else:
            print(f"❌ No player found with ID: {player_id}")


# ✅ Function to fetch player history
def fetch_player_history(player_id):
    """Fetches and prints player history from PlayerHistory."""
    with SessionLocal() as db_session:
        history = db_session.query(PlayerHistory).filter(PlayerHistory.PlayerID == player_id).all()

        if history:
            print(f"📜 History for Player ID {player_id}:")
            for record in history:
                print(f"- {record.Name}: Rating {record.Rating}, CTV {record.Transfervalue}, UpdatedAt {record.UpdatedAt}")
        else:
            print(f"❌ No history found for Player ID: {player_id}")


# ✅ Run Debugging Tests
if __name__ == "__main__":
    insert_test_player()
    fetch_all_players()
    update_player(1, {"Transfervalue": 1500})
    update_player(1, {"Transfervalue": 2000})
    fetch_player_history(1)
    delete_player(1)
