import pycountry
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Numeric
from Country import Country  # Importér din model
from Competition import Competition  # Importér din model


Base = declarative_base()

class Country(Base):
    __tablename__ = 'Country'
    
    Country_id = Column(Integer, primary_key=True)
    Name = Column(String(100), nullable=False)
    
    competitions = relationship("Competition", back_populates="country")
    #teams = relationship("Teams", back_populates="country")

class Competition(Base):
    __tablename__ = 'Competition'

    Competition_id = Column(Integer, primary_key=True)
    Competitionname = Column(String(100), nullable=False)
    divisionLevel = Column(Integer, nullable=False)
    country_fk_id = Column(Integer, ForeignKey("Country.Country_id"))
    
    country = relationship("Country", back_populates="competitions")
    #teams = relationship("Teams", back_populates="competition_team")

# Indlæs miljøvariabler fra .env-filen
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
        existing_count = session.query(Country).count()
        print(f"🔍 Found {existing_count} existing countries in database.")

        inserted_count = 0
        for c in pycountry.countries:
            country_name = c.name

            # Tjek om landet allerede findes i databasen
            existing_country = session.query(Country).filter_by(Name=country_name).first()
            if existing_country:
                print(f"⚠️ {country_name} already exists, skipping...")
                continue  # Spring over eksisterende lande

            # Tilføj nyt land
            session.add(Country(Name=country_name))
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
