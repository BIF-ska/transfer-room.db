import streamlit as st
import pandas as pd
import os
from pathlib import Path
import sys 
sys.path.append(str(Path(__file__).parents[1]))
sys.path.append(str(Path(__file__).parents[0]))
from sqlalchemy import create_engine
from dotenv import load_dotenv
import plotly.express as px

def run():
    load_dotenv()
    engine = create_engine(os.getenv("DATABASE_URL"))

    @st.cache_data
    def fetch_data():
        df = pd.read_sql("SELECT * FROM player_metrics", engine)

        # Make sure 'rating' exists and convert it
        if "rating" not in df.columns:
            st.error("Kolonnen 'rating' findes ikke i player_metrics-tabellen.")
            st.stop()

        df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
        return df

    st.title("⭐ Fordeling af spillere i Rating-grupper (Belgisk Liga)")

    data = fetch_data()

    if data['rating'].dropna().empty:
        st.warning("Ingen gyldige rating-data tilgængelige.")
    else:
        step = st.sidebar.slider("Vælg interval for rating-grupper:", min_value=5, max_value=20, value=10, step=5)
        min_rating = int(data['rating'].min() // step * step)
        max_rating = int(data['rating'].max() // step * step + step)
        bins = list(range(min_rating, max_rating + step, step))
        labels = [f"{i}-{i + step}" for i in bins[:-1]]

        data['rating_group'] = pd.cut(data['rating'], bins=bins, labels=labels, right=False)
        group_counts = data['rating_group'].value_counts().sort_index().reset_index()
        group_counts.columns = ['Rating Gruppe', 'Antal Spillere']

        st.dataframe(group_counts)

        fig = px.bar(group_counts, x="Rating Gruppe", y="Antal Spillere",
                     title="Rating-grupper for spillere i Belgisk Liga",
                     text="Antal Spillere",
                     color="Antal Spillere", color_continuous_scale="Tealgrn")
        st.plotly_chart(fig)
