from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.session import Session
import os


def database_session(fast_executemany=False) -> Session:
    """
    This function creates a database session.
    The database it connects to depends on the environment variable DATABASE_URL.

    Args:
        fast_executemany (bool, optional): Whether to use fast_executemany. Defaults to False.

    Returns:
        Session: The database session
    """
    try:
        # Retrieve the connection string from the environment variable
        connection_string = os.getenv('DATABASE_URL')
        if not connection_string:
            raise ValueError("DATABASE_URL not found in environment variables")

        # Create a database engine
        engine = create_engine(
            connection_string,
            connect_args={"fast_executemany": fast_executemany},
            isolation_level="READ COMMITTED",
            future=True
        )

        # Create a sessionmaker with explicit autocommit=False to disable autobegin
        db_session = sessionmaker(bind=engine, autoflush=True, autocommit=False, future=True)
        
        return db_session()
    except (SQLAlchemyError, ValueError) as e:
        print(f"An error occurred while creating a database session: {e}")
        return None