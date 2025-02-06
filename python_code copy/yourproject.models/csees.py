# seed_countries.py

import pycountry
import os
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import your models
from Country import Country
from Teams import Teams

load_dotenv()  # Loads DATABASE_URL from .env if present

def seed_countries():
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("No DATABASE_URL found.")
        return

    # Create engine and session
    engine = create_engine(db_url)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    try:
        # Insert country rows
        for c in pycountry.countries:
            session.add(Country(Name=c.name))
        session.commit()
        print("Countries inserted successfully.")
    except:
        session.rollback()
        raise
    finally:
        session.close()

# Only runs seed_countries() if this file is executed directly, not if imported.
if __name__ == "__main__":
    seed_countries()
