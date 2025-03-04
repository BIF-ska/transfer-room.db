import os
import sys
from fastapi import FastAPI, Depends, HTTPException, Header, Request
from fastapi.security.api_key import APIKeyHeader
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from databaseUrl import DATABASE_URL, SessionLocal
from typing import List
from agencyDTO import AgencyDTO

# ✅ Fix Import Issues (Ensure `internAPI` is Recognized)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))  # Add `internAPI/` to the search path

try:
    from Agencies import Agencies  # ✅ Import Agencies model
    print("✅ Successfully imported Agencies")
except Exception as e:
    print(f"❌ ERROR: Failed to import Agencies - {e}")

# ✅ Explicitly define `Agencies` globally
AGENCIES_MODEL = Agencies  # ✅ Assign Agencies to a global variable

# ✅ Load Environment Variables
load_dotenv()
API_KEY = os.getenv("API_KEY")

# ✅ Initialize FastAPI
app = FastAPI(title="Agencies API", description="Internal API with API Key Authentication", version="1.0.0")

# ✅ API Key Authentication
api_key_header = APIKeyHeader(name="api-key", auto_error=True)

def verify_api_key(request: Request, api_key: str = Header(None, alias="api-key")):
    query_api_key = request.query_params.get("api_key")  # Allow API key in URL
    received_key = api_key or query_api_key  # Use header first, then query param

    print(f"🔹 Received API Key: {repr(received_key)}")
    print(f"🔹 Expected API Key: {repr(API_KEY)}")

    if not received_key:
        raise HTTPException(status_code=400, detail="Missing API key")

    if received_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")

    return received_key

# ✅ Database Dependency
def get_db():
    """Dependency function to get a new database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ Fetch all agencies from the database
@app.get("/agencies", response_model=List[AgencyDTO])
def get_agencies(db: Session = Depends(get_db)):
    """Returns a list of all agencies."""
    try:
        print("✅ Checking if Agencies is accessible in this function...")
        print(f"✅ AGENCIES_MODEL: {AGENCIES_MODEL}")  # Debugging statement
        agencies = db.query(AGENCIES_MODEL).all()
        print(f"🔹 Retrieved Agencies: {agencies}")  # Debugging output
        return [AgencyDTO.model_validate(agency) for agency in agencies]
    except Exception as e:
        print(f"❌ ERROR: {e}")  # Print error to console
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
