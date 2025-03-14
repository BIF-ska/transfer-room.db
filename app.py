import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
import streamlit as st
import pandas as pd

# Load environment variables
load_dotenv()

# Get the database URL
db_url = os.getenv("DATABASE_URL")

# Create a connection engine
engine = create_engine(db_url)

# Function to fetch data
def fetch_data():
    query = "SELECT * from players"  # Change 'your_table' to your actual table name
    df = pd.read_sql(query, engine)
    return df

# Streamlit UI
st.title("MSSQL Database Viewer")

if st.button("Load Data"):
    data = fetch_data()
    st.dataframe(data)  # Display the data in an interactive table
