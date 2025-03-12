import os
import json
from concurrent.futures import ThreadPoolExecutor, as_completed





# ✅ Step 3: Insert Data into Database
def insert_data():
    """Inserts players and agencies into the database using TR_ID."""
   

    if not players_data:
        print("⚠️ No data to insert. Exiting.")
        return

    # Debug: Count total agencies & players in DB before inserting
    total_existing_agencies = session.query(Agencies).count()
    total_existing_players = session.query(Players).count()
    total_existing_links = session.query(PlayerAgency).count()

    # Fetch existing agencies
    existing_agencies = {agency.Agencyname: agency.id for agency in session.query(Agencies).all()}

    # Fetch Players mapping TR_ID to id (Primary Key)
    existing_players = {player.TR_ID: player.PlayerID for player in session.query(Players).all()}

    # Fetch existing Player-Agency relationships to prevent duplicates
    existing_links = {(link.player_id, link.agency_id) for link in session.query(PlayerAgency).all()}

    to_add = []

    for player_data in players_data:
        tr_id = player_data.get("TR_ID")  
        agency_name = player_data.get("Agency")
        agency_verified = player_data.get("AgencyVerified", False)

        if not tr_id or agency_name is None or agency_name.strip() == "":
            print(f"⚠️ Skipping invalid record: {player_data}")
            continue

        # Convert agency_verified properly
        agency_verified = str(agency_verified).lower() in ["yes", "true", "1"]

        # Ensure TR_ID exists in Players table
        if tr_id not in existing_players:
            print(f"⚠️ Skipping TR_ID {tr_id}, as they are not in the Players table.")
            continue

        player_id = existing_players[tr_id]  

        # Debug: Check if agency exists
        if agency_name in existing_agencies:
            agency_id = existing_agencies[agency_name]
        else:
            # Create new agency
            new_agency = Agencies(Agencyname=agency_name, Agencyverified=agency_verified)
            session.add(new_agency)
            session.flush()
            agency_id = new_agency.id
            existing_agencies[agency_name] = agency_id  # Store new agency ID

        # Debug: Print each linking attempt
        print(f"✅ Attempting to link Player {player_id} (TR_ID: {tr_id}) to Agency {agency_name} (ID: {agency_id})")

        # **Prevent Duplicate Insert**
        if (player_id, agency_id) not in existing_links:
            to_add.append(PlayerAgency(player_id=player_id, agency_id=agency_id))
            existing_links.add((player_id, agency_id))  # **Prevent inserting again**
        else:
            print(f"⚠️ Skipping duplicate entry for Player {player_id} and Agency {agency_name}")

    try:
        if to_add:
            session.bulk_save_objects(to_add)
            session.commit()
            print(f"✅ Inserted {len(to_add)} player-agency relationships.")
        else:
            print("⚠️ No valid player-agency records to insert.")
    except Exception as e:
        session.rollback()
        print(f"❌ Error committing transaction: {e}")
    finally:
        session.close()

    # Debug: Count total agencies & players in DB after inserting
    total_existing_agencies = session.query(Agencies).count()
    total_existing_players = session.query(Players).count()
    total_existing_links = session.query(PlayerAgency).count()
    print(f"📌 Agencies in DB after insert: {total_existing_agencies}")
    print(f"📌 Players in DB after insert: {total_existing_players}")
    print(f"📌 Player-Agency links after insert: {total_existing_links}")


# ✅ Step 4: Run with Threading
def threaded_insert():
    """Runs data insertion using multiple threads for efficiency."""
    with ThreadPoolExecutor(max_workers=5) as executor:
        future = executor.submit(insert_data)
        for f in as_completed([future]):
            print("✅ Data insertion completed.")

# ✅ Step 5: Query for Verification
def verify_data():
    """Checks if data is inserted correctly."""
    session = SessionLocal()
    
    players_with_agencies = session.query(PlayerAgency).all()
    
    if not players_with_agencies:
        print("⚠️ No player-agency relationships found.")
    else:
        print("✅ Player-Agency relationships:")
        for link in players_with_agencies[:10]:  # Show only first 10 for brevity
            print(f"Player {link.player_id} is linked to Agency {link.agency_id}")

    session.close()

# ✅ Run the program
if __name__ == "__main__":
    initialize_db()  # Ensure tables exist
    threaded_insert()  # Insert data with threading
    verify_data()  # Verify insertion
