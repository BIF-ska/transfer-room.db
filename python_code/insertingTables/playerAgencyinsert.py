import os
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from dotenv import load_dotenv

Base = declarative_base()

# ✅ Define the Agencies Table
class Agencies(Base):
    __tablename__ = "Agencies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    Agencyname = Column(String(255), nullable=False, unique=True)
    Agencyverified = Column(Boolean, default=False)

    # Relationship to PlayerAgency (Back Reference)
    players = relationship("PlayerAgency", back_populates="agency")

# ✅ Define the Players Table
class Players(Base):
    __tablename__ = "Players"

    PlayerID = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(255), nullable=False)  # Example player field
    TR_ID = Column(Integer, nullable=False)

    # Relationship to PlayerAgency (Back Reference)
    agencies = relationship("PlayerAgency", back_populates="player")

# ✅ Define the PlayerAgency Join Table
class PlayerAgency(Base):
    __tablename__ = "PlayerAgency"

    player_id = Column(Integer, ForeignKey("Players.PlayerID"), primary_key=True)
    agency_id = Column(Integer, ForeignKey("Agencies.id"), primary_key=True)

    # Define relationships to Players and Agencies
    player = relationship("Players", back_populates="agencies")
    agency = relationship("Agencies", back_populates="players")

    def __repr__(self):
        return f"<PlayerAgency(player_id={self.player_id}, agency_id={self.agency_id})>"

# ✅ Database setup
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in environment variables!")

engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ✅ Step 1: Create the Database Tables
def initialize_db():
    """Creates the database schema if it doesn't exist."""
    Base.metadata.create_all(engine)
    print("✅ Database tables created successfully.")

# ✅ Step 2: Load Data from JSON
def load_json_data():
    """Loads player-agency data from JSON file."""
    json_file_path = r"C:\Users\ska\OneDrive - Brøndbyernes IF Fodbold\Dokumenter\GitHub\transfer-room.db\players_data.json"

    try:
        with open(json_file_path, "r", encoding="utf-8") as file:
            return json.load(file)  # Load JSON into a Python list
    except Exception as e:
        print(f"❌ Error loading JSON file: {e}")
        return []

# ✅ Step 3: Insert Data into Database
def insert_data():
    """Inserts players and agencies into the database using TR_ID."""
    session = SessionLocal()
    players_data = load_json_data()

    if not players_data:
        print("⚠️ No data to insert. Exiting.")
        return

    # Fetch existing agencies
    existing_agencies = {agency.Agencyname: agency.id for agency in session.query(Agencies).all()}

    # Fetch Players mapping TR_ID to id (Primary Key)
    existing_players = {player.TR_ID: player.PlayerID for player in session.query(Players).all()}

    to_add = []

    for player_data in players_data:
        tr_id = player_data.get("TR_ID")  # Get TR_ID instead of player_id
        agency_name = player_data.get("Agency")
        agency_verified = player_data.get("AgencyVerified", False)

        if not tr_id or not agency_name:
            print(f"⚠️ Skipping invalid record: {player_data}")
            continue

        # Convert agency_verified properly
        agency_verified = str(agency_verified).lower() in ["yes", "true", "1"]

        # Ensure TR_ID exists in Players table
        if tr_id not in existing_players:
            print(f"⚠️ Skipping TR_ID {tr_id}, as they are not in the Players table.")
            continue

        player_id = existing_players[tr_id]  # Get the actual Player ID from the TR_ID

        # Check if agency exists, create if not
        if agency_name not in existing_agencies:
            new_agency = Agencies(Agencyname=agency_name, Agencyverified=agency_verified)
            session.add(new_agency)
            session.flush()  # Get the generated ID before commit
            existing_agencies[agency_name] = new_agency.id  # Store ID for reference

        # Create PlayerAgency link
        agency_id = existing_agencies[agency_name]
        print(f"✅ Linking Player {player_id} (TR_ID: {tr_id}) to Agency {agency_name} (ID: {agency_id})")
        to_add.append(PlayerAgency(player_id=player_id, agency_id=agency_id))

    try:
        if to_add:
            session.bulk_save_objects(to_add)
            session.commit()
            print(f"✅ Inserted {len(to_add)} player-agency relationships.")
        else:
            print("⚠️ No valid player-agency records to insert.")
    except Exception as e:
        session.rollback()
        print(f"❌ Error committing transaction: {e}")
    finally:
        session.close()

# ✅ Step 4: Run with Threading
def threaded_insert():
    """Runs data insertion using multiple threads for efficiency."""
    with ThreadPoolExecutor(max_workers=5) as executor:
        future = executor.submit(insert_data)
        for f in as_completed([future]):
            print("✅ Data insertion completed.")

# ✅ Step 5: Query for Verification
def verify_data():
    """Checks if data is inserted correctly."""
    session = SessionLocal()
    
    players_with_agencies = session.query(PlayerAgency).all()
    
    if not players_with_agencies:
        print("⚠️ No player-agency relationships found.")
    else:
        print("✅ Player-Agency relationships:")
        for link in players_with_agencies[:10]:  # Show only first 10 for brevity
            print(f"Player {link.player_id} is linked to Agency {link.agency_id}")

    session.close()

# ✅ Run the program
if __name__ == "__main__":
    initialize_db()  # Ensure tables exist
    threaded_insert()  # Insert data with threading
    verify_data()  # Verify insertion
