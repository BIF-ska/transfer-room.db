from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
import requests
from urllib.parse import urlencode

# Importer dine modeller
from Transferinfo import TransferInfo
from Players import Players  # Hvis transfers er knyttet til spillere

def seed_transfer_info():
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
        print(f"Error during authentication: {e}")
        return
    except ValueError as e:
        print(f"Error parsing token: {e}")
        return

    headers = {"Authorization": f"Bearer {token}"}
    request_url = "https://apiprod.transferroom.com/api/external/players"

    try:
        r = requests.get(request_url, headers=headers)
        r.raise_for_status()
        transfer_data = r.json()
        print(f"✅ Successfully fetched {len(transfer_data)} transfer records from API.")
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching transfer data: {e}")
        return

    for transfer in transfer_data:
        try:
            transfer_id = transfer.get("TR_ID")  # Hent transfer ID
            player_name = transfer.get("Name")  # Hent spillerens navn
            current_team = transfer.get("CurrentTeam")  # Hent nuværende team
            parent_team = transfer.get("ParentTeam")  # Hent tidligere team
            estimated_value = transfer.get("xTV")  # Forventet transfer værdi
            rating = transfer.get("Rating")  # Spillerens rating
            nationality = transfer.get("Nationality1")  # Spillerens nationalitet

            # ✅ Tjek om transferen allerede findes
            if not transfer_id or not player_name:
                print(f"⚠️ Skipping transfer {transfer_id} due to missing player name or transfer ID.")
                continue

            # ✅ Tjek om spilleren allerede findes
            player = db.query(Players).filter_by(Name=player_name).first()
            if not player:
                print(f"⚠️ Player '{player_name}' not found. Creating new player entry.")
                player = Players(Name=player_name, Nationality=nationality)
                db.add(player)
                db.commit()

            # ✅ Tjek om klubberne findes
            from_club = db.query(Clubs).filter_by(Name=parent_team).first()
            if not from_club:
                print(f"⚠️ Club '{parent_team}' not found. Creating new club entry.")
                from_club = Clubs(Name=parent_team)
                db.add(from_club)
                db.commit()

            to_club = db.query(Clubs).filter_by(Name=current_team).first()
            if not to_club:
                print(f"⚠️ Club '{current_team}' not found. Creating new club entry.")
                to_club = Clubs(Name=current_team)
                db.add(to_club)
                db.commit()

            # ✅ Sikre at transferen ikke allerede findes
            existing_transfer = db.query(TransferInfo).filter_by(TransferID=transfer_id).first()
            if existing_transfer:
                print(f"⚠️ Transfer {transfer_id} already exists. Skipping.")
                continue

            # ✅ Indsæt ny transfer
            new_transfer = TransferInfo(
                TransferID=transfer_id,
                TransferValue=estimated_value,
                PlayerID=player.PlayerID,
                FromClubID=from_club.ClubID,
                ToClubID=to_club.ClubID,
                Rating=rating
            )

            db.add(new_transfer)
            db.commit()
            print(f"✅ Successfully inserted: TransferID {transfer_id}")

        except Exception as e:
            db.rollback()
            print(f"❌ Error inserting Transfer {transfer_id}: {e}")

    db.close()

if __name__ == "__main__":
    seed_transfer_info()