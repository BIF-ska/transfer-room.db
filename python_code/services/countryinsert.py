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

def seed_countries():
    """Seeds the database with country data using the Database class."""
    db = Database()  
    session = db.get_session()

    try:
        existing_count = session.query(country).count()
        print(f"🔍 Found {existing_count} existing countries in the database.")

        inserted_count = 0

        for c in pycountry.countries:
            country_name = c.name

            existing_country = session.query(country).filter_by(country_name=country_name).first()
            if existing_country:
                print(f"⚠️ {country_name} already exists, skipping...")
                continue 

            new_country = country(country_name=country_name)
            session.add(new_country)
            inserted_count += 1
            print(f"✅ Inserted: {country_name}")

        session.commit()
        print(f"🎉 Successfully inserted {inserted_count} new countries.")

    except SQLAlchemyError as e:
        session.rollback()
        print(f"❌ Error inserting countries: {e}") 
    finally:
        session.close()
        db.dispose_engine() 
if __name__ == "__main__":
    seed_countries()