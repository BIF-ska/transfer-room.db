import sys
import os
import asyncio
from pathlib import Path
sys.path.append(str(Path(__file__).parents[1]))
sys.path.append(str(Path(__file__).parents[0]))
from util.database import Database
from sqlalchemy import create_engine
from sqlalchemy.orm import  sessionmaker
from dotenv import load_dotenv
from sqlalchemy.exc import SQLAlchemyError
from util.apiclient import APIClient
from models.competition import Competition
from models.country import country


SEMAPHORE = asyncio.Semaphore(10)  

async def fetch_competitions_from_api(api_client):
   
    return await api_client.fetch_competitions()

def seed_competitions():
    db = Database()
    session = db.get_session()

    api_client = APIClient()
    loop = asyncio.get_event_loop()
    competitions_data = loop.run_until_complete(fetch_competitions_from_api(api_client))

    if not competitions_data:
        print("❌ No data received from API or empty response!")
        return

    competitions_list = list(competitions_data)  

    print(f"Sample fetched competition: {competitions_list[:5]}")  

    unique_competitions = list({
        (comp.get("competitionName"), comp.get("country")): comp
        for comp in competitions_list if isinstance(comp, dict)
    }.values())

    if not unique_competitions:
        print("❌ No valid competition data found!")
        return

    existing_countries = {country.country_name: country for country in session.query(country).all()}
    existing_competitions = {(comp.competition_name, comp.country_id): comp for comp in session.query(Competition).all()}

    new_countries = []
    new_competitions = []

    for comp in unique_competitions:
        try:
            comp_name = comp.get("competitionName")
            division_level = comp.get("divisionLevel")
            country_name = comp.get("country")
            tr_id = comp.get("id")

            if not comp_name or not country_name or tr_id is None:
                print(f"⚠️ Skipping competition due to missing fields: {comp}")
                continue

            if country_name not in existing_countries:
                new_country = country(name=country_name)
                new_countries.append(new_country)
                existing_countries[country_name] = new_country  

            country_id = existing_countries[country_name].country_id

            if (comp_name, country_id) not in existing_competitions:
                new_competitions.append(
                    Competition(
                        competition_name=comp_name,
                        division_level=division_level,
                        country_id=country_id,
                        tr_id=tr_id
                    )
                )
            else:
                print(f"⚠️ Skipping existing competition: {comp_name} ({country_name})")

        except Exception as e:
            print(f"❌ Error processing competition: {e}")

    if new_countries:
        try:
            session.bulk_save_objects(new_countries)
            session.commit()
            print(f"✅ Inserted {len(new_countries)} new countries.")
        except SQLAlchemyError as e:
            print(f"❌ Error inserting countries: {e}")
            session.rollback()

    if new_competitions:
        try:
            session.bulk_save_objects(new_competitions)
            session.commit()
            print(f"✅ Successfully inserted {len(new_competitions)} new competitions!")
        except SQLAlchemyError as e:
            print(f"❌ Error committing competition batch insert: {e}")
            session.rollback()

    session.close()
    db.dispose_engine()

    print(f"✅ Summary: {len(new_competitions)} competitions inserted.")

if __name__ == "__main__":
    seed_competitions()
