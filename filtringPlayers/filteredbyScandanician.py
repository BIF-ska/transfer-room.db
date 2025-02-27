import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
from datetime import datetime

# 🔹 Load database credentials
load_dotenv()
db_url = os.getenv("DATABASE_URL")

if not db_url:
    print("❌ No DATABASE_URL found. Check your .env file.")
    exit()

# 🔹 Connect to database
engine = create_engine(db_url)

# 🔹 Corrected SQL Query
query = """
SELECT
    p.Name,
    p.BirthDate,
    p.FirstPosition AS Position,
    p.Rating,
    t.Teamname,
    p.ParentTeam,  -- Corrected: ParentTeam is now from players table
    c.Name AS Player_Country,
    team_country.Name AS Team_Country,
    p.Transfervalue
FROM players p
JOIN teams t ON p.fk_players_team = t.Team_id
JOIN country c ON p.player_Country_id = c.Country_id
JOIN country team_country ON t.Country_id = team_country.Country_id
WHERE
    c.Name IN ('Denmark', 'Norway', 'Sweden', 'Iceland', 'Finland')
    AND p.Rating BETWEEN 60 AND 85
    AND DATEDIFF(YEAR, p.BirthDate, GETDATE()) <= 32
    AND t.Country_id != (SELECT Country_id FROM country WHERE Name = 'Denmark');
"""

# 🔹 Fetch data into DataFrame
df = pd.read_sql(query, engine)

# 🔹 Generate filename with timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
file_name = f"filtered_scandinavian_players_{timestamp}.xlsx"

# 🔹 Save to Excel
df.to_excel(file_name, index=False)

print(f"✅ Data exported successfully: {file_name}")
