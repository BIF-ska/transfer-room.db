import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parents[1]))
sys.path.append(str(Path(__file__).parents[0]))

# Import database update functions
from agencyinsert import run_agency_update
from competitioninsert import seed_competitions
from playerinsert import run_player_update
from countryinsert import seed_countries
from playerAgencyinsert import update_player_agency
from teamsInsert import seed_teams

def run_all_updates():
    """Runs all update scripts in sequence."""
    print("🚀 Starting database updates...")

    try:

        print("🌍 Seeding Countries...")
        seed_countries()  # ✅ Function call fixed
        print("✅ Countries Updated!\n")
        
        print("🏆 Seeding Competitions...")
        seed_competitions()  # ✅ Function call fixed
        print("✅ Competitions Updated!\n")

      
        print("🏟️ Seeding Teams...")
        seed_teams()  # ✅ Function call fixed
        print("✅ Teams Updated!\n")

        print("🏢 Seeding Agencies...")
        run_agency_update()  # ✅ Function call fixed
        print("✅ Agencies Updated!\n")

        

        print("⚽ Seeding Players...")
        run_player_update()  # ✅ Function call fixed
        print("✅ Players Updated!\n")

        
        print("🤝 Seeding Player Agencies...")
        update_player_agency()  # ✅ Function call fixed
        print("✅ Player Agencies Updated!\n")


        print("🎉 All updates completed successfully!")

    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    run_all_updates()  # ✅ Corrected function call
