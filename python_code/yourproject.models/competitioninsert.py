#%%
import json
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from Competition import Competition # Importer begge modeller
from dotenv import load_dotenv
from Country import Country

# Læs miljøvariabler fra .env filen
load_dotenv() 

def seed_competition():
    # Hent database URL fra miljøvariablerne
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("No DATABASE_URL found.")
        return

    # Opret databaseforbindelse
    engine = create_engine(db_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    db = SessionLocal()  # Opret session
    
    # Åbn JSON-filen og læs data
    try:
        with open(r"C:\Users\sad\Documents\GitHub\transfer-room.db\python_code\yourproject.models\insertingTables\competitions.json", "r", encoding="utf-8") as file:
            data = json.load(file)
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        return

    # Debugging: Se hvad data indeholder
    print(type(data))  # Skal være <class 'list'>
    print(data[:2])  # Udskriver de første 2 elementer

    # Hvis data er en liste, fortsæt
    if isinstance(data, list):
        competition_list = data  # Data er en liste, brug den direkte
    else:
        raise ValueError("Uventet datastruktur i competitions.json!")

#%%
    # Indsæt data i databasen
    for comp in competition_list:
        print(f"Processing competition: {comp.get('competitionName')}") 

        # Tjek om konkurrencen allerede findes
        existing_comp = db.query(Competition).filter_by(Competition_id=comp["id"]).first()

        if not existing_comp:  # Undgå dubletter
            # Find Country objektet baseret på Country_id
            country = db.query(Country).filter_by(Name=comp['country']).first()
            
            if not country:
                print(f"Country with ID {comp['Country_id']} not found. Skipping competition.")
                country = Country(
                    country_id=comp["Country_id"],
                    name=comp["Country"]
                )
                db.flush(country)
                continue  # Hvis landet ikke findes, spring konkurrencen over

            # Opret ny Competition-instans med de korrekte kolonnenavne
            new_competition = Competition(
                Competition_id=comp["id"],  # Brug 'Competition_id' som den primære nøgle
                Competitioname=comp["Competitionname"],  # Brug 'Competitionname' som det korrekte kolonnenavn
                divisionLevel=comp["divisionLevel"],   # Denne virker fint
                Country_id=country.Country_id,  # Relater landet via Country_id
            )

            db.add(new_competition)  # Tilføj den nye competition til sessionen

    # Gem ændringer
    db.commit()
    db.close()  # Luk forbindelsen

    print("Competitions er nu importeret til databasen!")

# Kald funktionen for at starte processen
seed_competition()
