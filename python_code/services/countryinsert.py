import sys
import os 
from pathlib import Path

sys.path.append(str(Path(__file__).parents[1]))
sys.path.append(str(Path(__file__).parents[0]))

import pycountry
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.country import country

load_dotenv()

def seed_countries():
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("❌ No DATABASE_URL found in .env file.")
        return

    # Opret databaseforbindelse
    engine = create_engine(db_url)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    try:
        # Debug: Tæl eksisterende lande i databasen
        existing_count = session.query(country).count()
        print(f"🔍 Found {existing_count} existing countries in database.")

        inserted_count = 0
        for c in pycountry.countries:
            country_name = c.name

            # Tjek om landet allerede findes i databasen
            existing_country = session.query(country).filter_by(country_name=country_name).first()
            if existing_country:
                print(f"⚠️ {country_name} already exists, skipping...")
                continue  # Spring over eksisterende lande

            # Tilføj nyt land
            session.add(country(country_name=country_name))
            session.commit()  # Commit efter hver indsættelse for at undgå rollback
            inserted_count += 1
            print(f"✅ Inserted: {country_name}")

        print(f"🎉 Successfully inserted {inserted_count} new countries.")
    except Exception as e:
        session.rollback()
        print(f"❌ Error inserting countries: {e}") 
    finally:
        session.close()

if __name__ == "__main__":
    seed_countries()
