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
 
# 🔹 SQL Query to include Transfervalue
query = """
SELECT
    Name,
    BirthDate,
    FirstPosition AS Position,
    Rating,
    Transfervalue
FROM players
WHERE
    Rating BETWEEN 60 AND 85
    AND DATEDIFF(YEAR, BirthDate, GETDATE()) <= 27;  -- Spillere på 27 år eller yngre
"""
 
# 🔹 Fetch data into DataFrame
df = pd.read_sql(query, engine)
 
# 🔹 Filnavn med tidsstempel
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
file_name = f"filtered_players_with_transfervalue_{timestamp}.xlsx"
 
# 🔹 Save to Excel
df.to_excel(file_name, index=False)
 
print(f"✅ Data exported successfully: {file_name}")