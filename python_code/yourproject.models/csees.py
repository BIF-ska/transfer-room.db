import pycountry

# Import your custom session creation function
import  database_session_example 

import Country

def insert_all_countries():
    session = database_session()
    if not session:
        print("Could not create a session.")
        return

    try:
       

        for c in pycountry.countries:
            # Insert a new row for each country
            country_obj = Country(Name=c.name)
            session.add(country_obj)

        session.commit()
        print("All countries inserted successfully.")
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    insert_all_countries()
