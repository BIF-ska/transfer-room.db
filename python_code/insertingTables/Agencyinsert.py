import os
import json
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class Agencies(Base):
    __tablename__ = "Agencies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    Agencyname = Column(String(255), nullable=False, unique=True)
    Agencyverified = Column(Boolean, default=False)


def seed_agency():
    load_dotenv()
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("No DATABASE_URL found.")
        return

    engine = create_engine(db_url, echo=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    # Correctly load the JSON file
    json_file_path = r"C:\Users\ska\OneDrive - Brøndbyernes IF Fodbold\Dokumenter\GitHub\transfer-room.db\players_data.json"

    try:
        with open(json_file_path, "r", encoding="utf-8") as file:
            players_data = json.load(file)  # Load JSON into a Python object (list of dicts)
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        return

    existing_agencies = {agency.Agencyname for agency in db.query(Agencies.Agencyname).all()}

    for player in players_data:  # Now correctly iterating over JSON data (list of dictionaries)
        try:
            player_agency = player.get("Agency")  # Extract Agency name
            agency_verified = player.get("AgencyVerified", False)  # Extract AgencyVerified (default to False)

            # Convert to boolean
            agency_verified = True if str(agency_verified).lower() in ["yes", "true", "1"] else False  

            # Ensure agency is not duplicated before inserting
            if player_agency and player_agency not in existing_agencies:
                agency = Agencies(Agencyname=player_agency, Agencyverified=agency_verified)
                db.add(agency)
                existing_agencies.add(player_agency)
        except Exception as e:
            print(f"Error adding agency: {e}")
            db.rollback()

    try:
        db.commit()
    except Exception as e:
        print(f"Error committing transaction: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_agency()
