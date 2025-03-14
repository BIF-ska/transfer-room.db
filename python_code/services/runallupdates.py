import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parents[1]))
sys.path.append(str(Path(__file__).parents[0]))
import sys
from agencyinsert import run_agency_update
from competitioninsert import seed_competitions
from playerinsert import run_player_update
from countryinsert import seed_countries
from playerAgencyinsert import update_player_agency
from teamsInsert import seed_teams




def run_all_updates():
    """Runs all update scripts in sequence."""
    print("🚀 Starting database updates...")

    # ✅ Call each function directly instead of using subprocess
    try:
        print("🏢 Seeding Agencies...")
        run_agency_update
        print("✅ Agencies Updated!\n")

        print("🏆 Seeding Competitions...")
        seed_competitions()
        print("✅ Competitions Updated!\n")

        print("⚽ Seeding Players...")
        run_player_update
        print("✅ Players Updated!\n")

        print("🌍 Seeding Countries...")
        seed_countries()
        print("✅ Countries Updated!\n")

        print("🤝 Seeding Player Agencies...")
        update_player_agency
        print("✅ Player Agencies Updated!\n")

       

        print("🏟️ Seeding Teams...")
        seed_teams()
        print("✅ Teams Updated!\n")

        print("🎉 All updates completed successfully!")

    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    run_all_updates