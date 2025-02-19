from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
import requests
from urllib.parse import urlencode

# Importer dine modeller
from Transferinfo import TransferInfo  # Sørg for, at denne sti er korrekt
from Players import Players
from Playersinfo import PlayersInfo  # Korrekt sti til din PlayersInfo-model
from Country import Country


from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class TransferInfo(Base):
    __tablename__ = "TransferInfo"

    TransferID = Column(Integer, primary_key=True, autoincrement=True)
    TransferValue = Column(Integer, nullable=False)

    # Relationships
    players_info = relationship("PlayersInfo", back_populates="transfer_info")

class Players(Base):
    __tablename__ = "Players"
    
    PlayerID = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String, nullable=False)
    Nationality = Column(String, nullable=True)

    # Relationships
    players_info = relationship("PlayersInfo", back_populates="player")

class PlayersInfo(Base):
    __tablename__ = "PlayersInfo"

    PlayersInfoID = Column(Integer, primary_key=True, autoincrement=True)  # Sørg for korrekt primær nøgle
    TransferID = Column(Integer, ForeignKey('TransferInfo.TransferID'), nullable=False)
    PlayerID = Column(Integer, ForeignKey('Players.PlayerID'), nullable=False)
    Rating = Column(Integer, nullable=True)  # assuming rating is a number

    # Relationships
    transfer_info = relationship("TransferInfo", back_populates="players_info")
    player = relationship("Players", back_populates="players_info")



def seed_transfer_info():
    load_dotenv()

    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("❌ No DATABASE_URL found.")
        return

    engine = create_engine(db_url, echo=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    # Få API-token
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
    request_url = "https://apiprod.transferroom.com/api/external/transfers"  # Eksempel på endpoint til transferinfo

    try:
        r = requests.get(request_url, headers=headers)
        r.raise_for_status()
        transfer_info_data = r.json()
        print(f"✅ Successfully fetched {len(transfer_info_data)} transfer info records from API.")
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching transfer info data: {e}")
        return

    for transfer_info in transfer_info_data:
        try:
            transfer_id = transfer_info.get("TR_ID")
            transfer_value = transfer_info.get("xTV")

            if not transfer_id or not transfer_value:
                print(f"⚠️ Skipping transfer info {transfer_id} due to missing values.")
                continue

            # ✅ Tjek om transferen allerede findes
            existing_transfer = db.query(TransferInfo).filter_by(TransferID=transfer_id).first()
            if existing_transfer:
                print(f"⚠️ Transfer {transfer_id} already exists. Skipping.")
                continue

            # ✅ Indsæt ny transfer info
            new_transfer_info = TransferInfo(
                TransferID=transfer_id,
                TransferValue=transfer_value
            )

            db.add(new_transfer_info)
            db.commit()
            print(f"✅ Successfully inserted: TransferID {transfer_id}")

        except Exception as e:
            db.rollback()
            print(f"❌ Error inserting TransferInfo {transfer_id}: {e}")

    db.close()

