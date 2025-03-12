import sys
import os 
from pathlib import Path

sys.path.append(str(Path(__file__).parents[1]))
sys.path.append(str(Path(__file__).parents[0]))
from util.database import Database
import pycountry
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from models.country import country

load_dotenv()
def seed_countries():
    """Seeds the database with country data using the Database class."""
    db = Database()  # Use the Database class
    session = db.get_session()

    try:
        # Debug: Count existing countries in the database
        existing_count = session.query(country).count()
        print(f"🔍 Found {existing_count} existing countries in the database.")

        inserted_count = 0

        for c in pycountry.countries:
            country_name = c.name

            # Check if the country already exists in the database
            existing_country = session.query(country).filter_by(country_name=country_name).first()
            if existing_country:
                print(f"⚠️ {country_name} already exists, skipping...")
                continue  # Skip existing countries

            # Add new country
            new_country = country(country_name=country_name)
            session.add(new_country)
            inserted_count += 1
            print(f"✅ Inserted: {country_name}")

        # Commit all changes at once for better performance
        session.commit()
        print(f"🎉 Successfully inserted {inserted_count} new countries.")

    except SQLAlchemyError as e:
        session.rollback()
        print(f"❌ Error inserting countries: {e}") 
    finally:
        session.close()
        db.dispose_engine()  # Dispose the database connection when done

if __name__ == "__main__":
    seed_countries()