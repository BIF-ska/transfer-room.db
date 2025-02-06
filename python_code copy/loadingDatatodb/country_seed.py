import pycountry

# Import the session creation function
from database_session_example import database_session

# Import your Country model
from python_code.yourproject.models import Country


def insert_all_countries():
    # 1) Get a Session from your existing function
    session = database_session()
    if not session:
        print("Could not create a session. Exiting.")
        return

    # 2) Insert data
    try:
        for c in pycountry.countries:
            # For example, store the name in the 'Name' column
            country_obj = Country(Name=c.name)
            session.add(country_obj)

        # 3) Commit the transaction
        session.commit()
        print("All countries inserted successfully.")

    except Exception as e:
        session.rollback()
        print(f"Error inserting countries: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    insert_all_countries()
