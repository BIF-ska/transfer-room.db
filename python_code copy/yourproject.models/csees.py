# seed_countries.py

import pycountry
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import Country
import os

def seed_countries():
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("No DATABASE_URL found.")
        return
    engine = create_engine(db_url)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()



    try:
        for c in pycountry.countries:
            session.add(Country(Name=c.name))
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

if __name__ == "__main__":
    seed_countries()
    print("Countries seeded.")
