import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

class Database:
    def __init__(self):
        
        load_dotenv()
        self.db_url = os.getenv("DATABASE_URL")

        if not self.db_url:
            raise ValueError(" No DATABASE_URL found in .env file.")

        # Create engine and session factory
        self.engine = create_engine(self.db_url, echo=False)
        self.SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=self.engine))

    def get_session(self):
        """Provides a new session."""
        return self.SessionLocal()

    def close_session(self):
        self.SessionLocal.remove()

    def dispose_engine(self):
        self.engine.dispose()

