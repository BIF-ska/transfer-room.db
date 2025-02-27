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

# 🔹 Updated SQL Query (Without Team_Country_ID)
query = """
SELECT
    p.Name,
    p.BirthDate,
    p.FirstPosition AS Position,
    p.Rating,
    p.Transfervalue,
    p.ParentTeam,
    t.Teamname,
    team_country.Name AS Team_Country,  
    c.Name AS Player_Country,
    p.Nationality1,
    p.Nationality2
FROM players p
LEFT JOIN teams t ON p.fk_players_team = t.Team_id
LEFT JOIN country c ON p.player_Country_id = c.Country_id
LEFT JOIN country team_country ON t.Country_id = team_country.Country_id  -- Join to get team country name

WHERE
    p.Rating BETWEEN 60 AND 85
    AND DATEDIFF(YEAR, p.BirthDate, GETDATE()) <= 27;  -- Players aged 27 or younger
"""

# 🔹 Fetch data into DataFrame
df = pd.read_sql(query, engine)

# 🔹 Generate filename with timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
file_name = f"filtered_players_with_transfervalue_{timestamp}.xlsx"

# 🔹 Save to Excel
df.to_excel(file_name, index=False)

print(f"✅ Data exported successfully: {file_name}")
