import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Load .env
load_dotenv()
db_url = os.getenv("DATABASE_URL")
engine = create_engine(db_url)

# Hent data
@st.cache_data
def fetch_data():
    query = "SELECT * FROM players"
    df = pd.read_sql(query, engine)
    df['birth_date'] = pd.to_datetime(df['birth_date'], errors='coerce')
    df['age'] = df['birth_date'].apply(lambda x: datetime.now().year - x.year if pd.notnull(x) else None)
    return df

# Streamlit UI
st.title("MSSQL Database Viewer")

if st.button("Load Data"):
    data = fetch_data()
    st.dataframe(data)  # Display the data in an interactive table
