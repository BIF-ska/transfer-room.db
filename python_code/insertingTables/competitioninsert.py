import os
import requests
from dotenv import load_dotenv
from urllib.parse import urlencode

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Numeric
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

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


def seed_competitions():
    load_dotenv()

    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("❌ No DATABASE_URL found.")
        return

    engine = create_engine(db_url, echo=True)
    engine.dispose()

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    email = os.getenv("email")
    password = os.getenv("password")
    base_url = os.getenv("base_url")
    params = {'email': email, 'password': password}
    auth_url = f"{base_url}?{urlencode(params)}"

    try:
        r = requests.post(auth_url)
        r.raise_for_status()
        token_json_data = r.json()
        token = token_json_data.get('token')
        if not token:
            raise ValueError("Token not found in the API response.")
    except requests.exceptions.RequestException as e:
        print(f"Error during authentication: {e}")
        return
    except ValueError as e:
        print(f"Error parsing token: {e}")
        return

    headers = {"Authorization": f"Bearer {token}"}
    request_url = "https://apiprod.transferroom.com/api/external/competitions"

    try:
        r = requests.get(request_url, headers=headers)
        r.raise_for_status()
        competitions_data = r.json()
        print(f"✅ Successfully fetched {len(competitions_data)} competitions from API.")
    except requests.exceptions.RequestException as e: 
        print(f"❌ Error fetching competition data: {e}")
        return

    for comp in competitions_data:
        try:
            comp_name = comp.get("competitionName")
            division_level = comp.get("divisionLevel")
            country_name = comp.get("country")

            if not comp_name or not country_name:
                print(f"⚠️ Skipping competition due to missing name or country.")
                continue

            # ✅ Hent eller opret land
            country = db.query(Country).filter_by(Name=country_name).first()
            if not country:
                print(f"🆕 Creating new country: {country_name}")
                country = Country(Name=country_name)
                db.add(country)
                db.commit()
                db.refresh(country)

            # ✅ Sikre at konkurrencen ikke allerede findes
          

            # ✅ Indsæt ny konkurrence
            new_competition = Competition(
              
                Competitionname=comp_name,
                divisionLevel=division_level,
                country_fk_id=country.Country_id
            )

            db.add(new_competition)
            db.commit()
            print(f"✅ Successfully inserted: {comp_name}")

        except Exception as e:
            db.rollback()
            print(f"❌ Error inserting competition {comp_name}: {e}")

    db.close()

if __name__ == "__main__":
    seed_competitions()
