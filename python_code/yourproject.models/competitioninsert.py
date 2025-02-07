#%%
import json
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv() 

def seed_competition():

    from Country import Country  # Import both models
    from Competition import Competition  # Import both models

    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("No DATABASE_URL found.")
        return

    # Create database connection
    engine = create_engine(db_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    db = SessionLocal()  # Create session
    
    # Open JSON file and read data
    try:
        with open(r"C:\Users\ska\OneDrive - Brøndbyernes IF Fodbold\Dokumenter\GitHub\transfer-room.db\python_code\yourproject.models\insertingTables\competitions.json") as file:
            data = json.load(file)
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        return

    # Debugging: Check what data contains
    print(type(data))  # Should be <class 'list'>
    print(data[:2])  # Print the first 2 elements

    # If data is a list, continue
    if isinstance(data, list):
        competition_list = data  # Data is a list, use it directly
    else:
        raise ValueError("Unexpected data structure in competitions.json!")

#%%
    # Insert data into database
    for comp in competition_list:
        print(f"Processing competition: {comp.get('Competitionname')}")  

        # Check if competition already exists
        existing_comp = db.query(Competition).filter_by(Competition_id=comp["id"]).first()

        if not existing_comp:  # Avoid duplicates
            # Find Country object based on Country_id
            country = db.query(Country).filter_by(Name=comp['country']).first()

            
            if not country:
                print(f"Country with Name {comp['Country']} not found. Creating a new country entry.")
                country = Country(
                    Country_id=comp["Country_id"],
                    Name=comp["Country"]
                )
                db.add(country)
                db.flush()  # Ensure the country is saved before continuing

            # Create a new Competition instance with the correct column names
            new_competition = Competition(
    Competition_id=comp["id"],  # ✅ Use JSON "id" to match SQLAlchemy "Competition_id"
    Competitionname=comp["competitionName"],  # ✅ Ensure correct key mapping
    divisionLevel=comp["divisionLevel"]
)


            db.add(new_competition)  # Add the new competition to the session

    # Commit changes
    db.commit()
    db.close()  # Close connection

    print("Competitions have been imported into the database!")

# Call the function to start the process
seed_competition()
