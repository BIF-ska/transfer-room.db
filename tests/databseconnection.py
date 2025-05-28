import pyodbc

try:
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost,1433;"
        "UID=sa;"
        "PWD=StrongPassword123;"
        "DATABASE=transferRoom_new"
    )
    print("✅ Connected to SQL Server")
except Exception as e:
    print("❌ Connection failed:", e)
