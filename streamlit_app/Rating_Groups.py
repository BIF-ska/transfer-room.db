import streamlit as st
import pandas as pd
import os
from pathlib import Path
import sys
from sqlalchemy import create_engine
from dotenv import load_dotenv
import plotly.express as px

# Tilføj projektmappen til path
sys.path.append(str(Path(__file__).parents[1]))
sys.path.append(str(Path(__file__).parents[0]))

def run():
    load_dotenv()
    engine = create_engine(os.getenv("DATABASE_URL"))

    @st.cache_data
    def fetch_data():
        players = pd.read_sql("SELECT * FROM players", engine)
        metrics = pd.read_sql("SELECT * FROM player_metrics", engine)
        competitions = pd.read_sql("SELECT * FROM competition", engine)

        # Ensart datatype på competition_id før merge
        players['competition_id'] = players['competition_id'].astype(str)
        competitions['competition_id'] = competitions['competition_id'].astype(str)

        # Merge players med competition (via competition_id)
        players = pd.merge(players, competitions, on="competition_id", how="left")

        # Merge players + metrics via player_id (outer for at bevare alt)
        df = pd.merge(players, metrics, on="player_id", how="left")

        # Sørg for numeric rating
        if "rating" in df.columns:
            df['rating'] = pd.to_numeric(df['rating'], errors='coerce')

        return df

    st.title("⭐ Rating-grupper på tværs af ligaer")
    data = fetch_data()

    # Debug: vis ligatilgængelighed
    st.sidebar.markdown("### Debug: Ligaoversigt")
    st.sidebar.write("Antal ligaer i data:", data['competition_name'].nunique())
    st.sidebar.dataframe(data['competition_name'].value_counts())

    # Filtrér liga
    ligaer = sorted(data['competition_name'].dropna().unique().tolist())
    valgt_liga = st.sidebar.selectbox("Vælg liga", ["Alle"] + ligaer)

    if valgt_liga != "Alle":
        data = data[data['competition_name'] == valgt_liga]

    # Sørg for at rating eksisterer
    if 'rating' not in data.columns or data['rating'].dropna().empty:
        st.warning("Ingen gyldige rating-data tilgængelige.")
        return

    # Rating-gruppe logik
    step = st.sidebar.slider("Interval for rating-grupper:", min_value=5, max_value=20, value=10, step=5)
    min_rating = int(data['rating'].min() // step * step)
    max_rating = int(data['rating'].max() // step * step + step)
    bins = list(range(min_rating, max_rating + step, step))
    labels = [f"{i}-{i + step}" for i in bins[:-1]]

    data['rating_group'] = pd.cut(data['rating'], bins=bins, labels=labels, right=False)
    group_counts = data['rating_group'].value_counts().sort_index().reset_index()
    group_counts.columns = ['Rating Gruppe', 'Antal Spillere']

    st.subheader(f"📊 Fordeling af spillere i rating-grupper{f' – {valgt_liga}' if valgt_liga != 'Alle' else ''}")
    st.dataframe(group_counts)

    fig = px.bar(group_counts,
                 x="Rating Gruppe",
                 y="Antal Spillere",
                 title=f"Rating-grupper for spillere{f' i {valgt_liga}' if valgt_liga != 'Alle' else ' i alle ligaer'}",
                 text="Antal Spillere",
                 color="Antal Spillere",
                 color_continuous_scale="Tealgrn")
    st.plotly_chart(fig)
