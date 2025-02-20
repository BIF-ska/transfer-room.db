import os
import json
from urllib.parse import urlencode
import requests
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Numeric
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy import Column, Integer, String, Boolean, Date

Base = declarative_base()

class Agencies(Base):
    __tablename__ = "Agencies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    Agencyname = Column(String(255), nullable=False, unique=True)
    Agencyverified = Column(Boolean, default=False)

    # Relationships
    player = relationship("Player")
    agency = relationship("Agency")
    coaches = relationship("HeadCoach", back_populates="agency")

class HeadCoach(Base):
    __tablename__ = 'HeadCoach'

    CoachID = Column(Integer, primary_key=True)
    Name = Column(String(100))
    BirthDate = Column(Date)
    Nationality1 = Column(String(100))
    Nationality2 = Column(String(100), nullable=True)
    CurrentRole = Column(String(100))
    ContractExpiry = Column(Date)
    fk_Head_Coach = Column(Integer, ForeignKey('agencies.AgencyID'))




# --- Seeding Function ---
def seed_headcoach():
    # --- Load environment variables ---
    load_dotenv()
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("❌ No DATABASE_URL found. Check your .env file.")
        return
    print("✅ DATABASE_URL loaded successfully.")

    # --- Set up the database engine and session ---
    engine = create_engine(db_url, echo=True)  # echo=True prints SQL statements for debugging.
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

    # --- Fetch HeadCoach Data ---
    request_url = 'https://apiprod.transferroom.com/api/external/coaches'  # Double-check API URL
    try:
        r = requests.get(request_url, headers=headers)
        r.raise_for_status()
        headcoach_data = r.json()

        # Print out the structure of the fetched data for debugging
        print(json.dumps(headcoach_data, indent=4))  # See what data looks like
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching head coach data: {e}")
        return

    # --- Process and Insert Data into the Database ---
    try:
        for coach in headcoach_data:
            # Check if agency exists, and insert if not
            agency_name = coach['Agencyname']  # Assuming 'agency_name' exists in the data
            agency = db.query(Agencies).filter_by(Agencyname=agency_name).first()

            if not agency:
                # Insert new agency
                agency = Agencies(Agencyname=agency_name, Agencyverified=True)
                db.add(agency)
                db.commit()

            # Insert new HeadCoach
            new_coach = HeadCoach(
                CoachID=coach['coach_id'],  # Assuming 'coach_id' exists in the data
                Name=coach['name'],  # Assuming 'name' exists in the data
                BirthDate=coach.get('birthdate', None),  # Optional field
                Nationality1=coach.get('nationality1', None),  # Optional field
                Nationality2=coach.get('nationality2', None),  # Optional field
                CurrentRole=coach.get('current_role', None),  # Optional field
                ContractExpiry=coach.get('contract_expiry', None),  # Optional field
                fk_Head_Coach=agency.id  # Foreign key relation
            )

            db.add(new_coach)
        db.commit()
        print("✅ Head coaches have been added successfully!")
    except IntegrityError as e:
        print(f"❌ Error inserting into database: {e}")
        db.rollback()  # Rollback in case of error

    finally:
        db.close()  # Make sure to close the database session

# Call the seed function to execute the script
seed_headcoach()
