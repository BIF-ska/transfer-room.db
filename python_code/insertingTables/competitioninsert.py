import json
import os
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

# Define the Base class
Base = declarative_base()

# Define the Country class
class Country(Base):
    __tablename__ = 'Country'
    
    Country_id = Column(Integer, primary_key=True)
    Name = Column(String(100), nullable=False)
    
    # Relationship to Competition
    competitions = relationship("Competition", back_populates="country")

# Define the Competition class
class Competition(Base):
    __tablename__ = 'Competition'

    Competition_id = Column(Integer, primary_key=True)
    Competitionname = Column(String(100), nullable=False)
    divisionLevel = Column(Integer, nullable=False)
    country_fk_id = Column(Integer, ForeignKey("Country.Country_id"))  # Correct column name

    # Relationship to Country
    country = relationship("Country", back_populates="competitions")
    
    load_dotenv()

def seed_competition():
    print("Starting the seeding process...")

    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("❌ No DATABASE_URL found. Check your .env file.")
        return

    print(f"✅ DATABASE_URL loaded successfully.")

    engine = create_engine(db_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    json_path = r"C:\Users\ska\OneDrive - Brøndbyernes IF Fodbold\Dokumenter\GitHub\transfer-room.db\python_code\yourproject.models\insertingTables\competitions.json"
    
    try:
        with open(json_path, "r") as file:
            data = json.load(file)
    except Exception as e:
        print(f"❌ Error reading JSON file: {e}")
        return

    if not isinstance(data, list):
        print("❌ Unexpected JSON format!")
        return

    error_count = 0  # Track number of errors

    for comp in data:
        print(f"🔄 Processing competition: {comp.get('competitionName')} (ID: {comp.get('id')})")

        try:
            existing_comp = db.query(Competition).filter_by(Competition_id=comp["id"]).first()
            if existing_comp:
                print(f"⚠️ Competition {comp['competitionName']} already exists. Skipping.")
                continue
        except Exception as e:
            print(f"❌ Error querying competition {comp['id']}: {e}")
            error_count += 1
            continue

        try:
            country = db.query(Country).filter_by(Name=comp['country']).first()
            if not country:
                print(f"🆕 Creating new country: {comp['country']}")
                country = Country(
                    Country_id=comp["id"],  # Assuming "id" is the country ID
                    Name=comp["country"]
                )
                db.add(country)
                db.flush()  # Ensure the country ID is available

            new_competition = Competition(
                Competition_id=comp["id"],
                Competitionname=comp["competitionName"],
                divisionLevel=comp["divisionLevel"],
                country_fk_id=country.Country_id  # Use the correct column name
            )
            db.add(new_competition)
            print(f"✅ Added competition {comp['competitionName']}")

        except Exception as e:
            print(f"❌ Error adding competition {comp['competitionName']}: {e}")
            error_count += 1
            continue

    # Try to commit all changes
    try:
        db.commit()
        if error_count > 0:
            print(f"⚠️ Import finished with {error_count} errors.")
        else:
            print("✅ All competitions have been imported successfully!")
    except Exception as e:
        print(f"❌ Error committing changes: {e}")
    finally:
        db.close()

# Run the function
seed_competition()