import streamlit as st
import pandas as pd
import os
from pathlib import Path
import sys 
sys.path.append(str(Path(__file__).parents[1]))
sys.path.append(str(Path(__file__).parents[0]))
from sqlalchemy import create_engine
from dotenv import load_dotenv
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go 

def run():
    load_dotenv()
    engine = create_engine(os.getenv("DATABASE_URL"))

    @st.cache_data
    def fetch_data():
        # Fetching data from the database
        df = pd.read_sql("SELECT * FROM players", engine)
        df['birth_date'] = pd.to_datetime(df['birth_date'], errors='coerce')
        df['age'] = df['birth_date'].apply(lambda x: datetime.now().year - x.year if pd.notnull(x) else None)
        return df

    st.title("🔍 Filtrering & Oversigt")

    data = fetch_data()

    
    # Sidebar filters
    st.sidebar.header("Filtre")
    search_name = st.sidebar.text_input("🔎 Søg efter spillerens navn:")
    selected_country = st.sidebar.selectbox("Vælg land:", ["Alle"] + sorted(data['nationality1'].dropna().unique()))
    selected_team = st.sidebar.selectbox("Vælg klub:", ["Alle"] + sorted(data['parent_team'].dropna().unique()))

    filtered_data = data.copy()
    if search_name:
        filtered_data = filtered_data[filtered_data['player_name'].str.contains(search_name, case=False, na=False)]
    if selected_country != "Alle":
        filtered_data = filtered_data[filtered_data['nationality1'] == selected_country]
    if selected_team != "Alle":
        filtered_data = filtered_data[filtered_data['parent_team'] == selected_team]

    st.write(f"Viser **{len(filtered_data)}** spillere ud af {len(data)}")

    # Nationality Distribution
    st.subheader("📌 Nationalitetsfordeling")
    nat_count = filtered_data['nationality1'].value_counts().reset_index()
    nat_count.columns = ['Nationality', 'Count']
    fig1 = px.bar(nat_count, x='Nationality', y='Count', title="Antal spillere pr. nationalitet")
    st.plotly_chart(fig1)

   


    # Position Distribution
    st.subheader("⚽ Fordeling af positioner")
    pos_count = filtered_data['first_position'].value_counts()
    fig2 = px.pie(names=pos_count.index, values=pos_count.values, title='Positioner fordelt')
    st.plotly_chart(fig2)

    # Age Distribution
    st.subheader("🎂 Aldersfordeling")
    fig3 = px.histogram(filtered_data, x='age', nbins=20, title='Aldersfordeling af spillere')
    st.plotly_chart(fig3)

    # Top 10 Clubs
    st.subheader("🏟️ Spillere pr. klub")
    club_counts = filtered_data['parent_team'].value_counts().head(10).reset_index()
    club_counts.columns = ['Team', 'Player Count']
    fig4 = px.bar(club_counts, x='Team', y='Player Count', title='Top 10 klubber med flest spillere')
    st.plotly_chart(fig4)

    # Heatmap Position vs Nationality
    st.subheader("🌍 Heatmap: Position vs. Nationalitet")
    heat_data = filtered_data.groupby(['first_position', 'nationality1']).size().reset_index(name='count')
    fig_heat = px.density_heatmap(
        heat_data,
        x="nationality1",
        y="first_position",
        z="count",
        color_continuous_scale="Viridis",
        title="Positioner fordelt på nationaliteter"
    )
    st.plotly_chart(fig_heat)

    # Average Age by Position
    st.subheader("🎂 Gennemsnitsalder pr. position")
    age_pos = filtered_data.groupby("first_position")["age"].mean().reset_index()
    fig_age_pos = px.bar(age_pos, x="first_position", y="age", title="Gennemsnitsalder pr. position")
    st.plotly_chart(fig_age_pos)

    # Birth Year Distribution
    st.subheader("📆 Fødselsår")
    filtered_data["birth_year"] = filtered_data["birth_date"].dt.year
    fig_birth = px.histogram(filtered_data, x="birth_year", nbins=20, title="Fødselsår for spillere")
    st.plotly_chart(fig_birth)

    # Handling Agencies and Player Agencies
    agencies_df = pd.read_sql("SELECT * FROM agencies", engine)
    player_agency_df = pd.read_sql("SELECT * FROM player_agency", engine)

    # Step 1: Merge player_agency and agencies data
    merged_data = pd.merge(player_agency_df, agencies_df, left_on='agency_id', right_on='agency_id')

    # Step 2: Count number of players per agency
    player_count_per_agency = merged_data.groupby('agency_name').size().reset_index(name='player_count')

    # Step 3: Create a bar chart showing the number of players per agency
    fig_agency = px.bar(player_count_per_agency, 
                        x='agency_name', 
                        y='player_count',
                        title="Number of Players per Agency",
                        labels={'agency_name': 'Agency', 'player_count': 'Number of Players'},
                        color='player_count', 
                        color_continuous_scale='Viridis')

    st.plotly_chart(fig_agency)
