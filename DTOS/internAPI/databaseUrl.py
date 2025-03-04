import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# ✅ Load environment variables
load_dotenv()

# ✅ Read DATABASE_URL from .env
DATABASE_URL = os.getenv("DATABASE_URL")

# ✅ Create database engine
engine = create_engine(DATABASE_URL)

# ✅ Create a database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
