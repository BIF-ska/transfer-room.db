import os
import requests
from dotenv import load_dotenv
from urllib.parse import urlencode
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

class Country(Base):
    __tablename__ = 'Country'
    
    Country_id = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(100), nullable=False, unique=True)
    
    competitions = relationship("Competition", back_populates="country")

class Competition(Base):
    __tablename__ = 'Competition'

    Competition_id = Column(Integer, primary_key=True, autoincrement=True)
    Competitionname = Column(String(100), nullable=False)
    divisionLevel = Column(Integer, nullable=False)
    country_fk_id = Column(Integer, ForeignKey("Country.Country_id"))
    TR_compID = Column(Integer, nullable=False)
    
    country = relationship("Country", back_populates="competitions")

def seed_competitions():
    load_dotenv()

    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("❌ No DATABASE_URL found.")
        return

    engine = create_engine(db_url, echo=True)
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
        print(f"❌ Error during authentication: {e}")
        return
    except ValueError as e:
        print(f"❌ Error parsing token: {e}")
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

    inserted_count = 0
    skipped_count = 0

    # ✅ Use a dictionary that includes both competition name + country to avoid removing valid entries
    unique_competitions = {(comp["competitionName"], comp["country"]): comp for comp in competitions_data}.values()

    for comp in unique_competitions:
        try:
            comp_name = comp.get("competitionName")
            division_level = comp.get("divisionLevel")
            country_name = comp.get("country")
            TR_ID = comp.get("id")  
            
            if not comp_name or not country_name or TR_ID is None:
                print(f"⚠️ Skipping competition due to missing fields: {comp}")
                skipped_count += 1
                continue

            # ✅ Find or create the country
            country = db.query(Country).filter_by(Name=country_name).first()
            if not country:
                print(f"🆕 Creating new country: {country_name}")
                country = Country(Name=country_name)
                db.add(country)
                db.flush()  
                db.refresh(country)

            # ✅ Check if the competition exists using `Competitionname` + `country_fk_id`
            existing_competition = db.query(Competition).filter(
                Competition.Competitionname == comp_name,
                Competition.country_fk_id == country.Country_id
            ).first()

            if not existing_competition:
                # ✅ Insert new competition
                new_competition = Competition(
                    Competitionname=comp_name,
                    divisionLevel=division_level,
                    country_fk_id=country.Country_id,
                    TR_compID=TR_ID
                )

                db.add(new_competition)
                db.commit()
                inserted_count += 1
                print(f"✅ Inserted: {comp_name} ({country_name}) - TR_compID: {TR_ID}")
            else:
                print(f"⚠️ Skipping existing competition: {comp_name} ({country_name})")
                skipped_count += 1

        except Exception as e:
            db.rollback()
            print(f"❌ Error inserting competition {comp_name}: {e}")

    db.close()
    print(f"✅ Summary: {inserted_count} competitions inserted, {skipped_count} skipped.")

if __name__ == "__main__":
    seed_competitions()
