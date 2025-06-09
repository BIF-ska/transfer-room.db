import streamlit as st
import pandas as pd
import os
from pathlib import Path
import sys
from sqlalchemy import create_engine
from dotenv import load_dotenv
from datetime import datetime
import plotly.express as px

# Tilføj projektmappen til path hvis nødvendigt
sys.path.append(str(Path(__file__).parents[1]))
sys.path.append(str(Path(__file__).parents[0]))

def run():
    load_dotenv()
    engine = create_engine(os.getenv("DATABASE_URL"))

    @st.cache_data
    def fetch_data():
        players = pd.read_sql("SELECT * FROM players", engine)
        metrics = pd.read_sql("SELECT * FROM player_metrics", engine)

        # Konverter dato og alder
        players['birth_date'] = pd.to_datetime(players['birth_date'], errors='coerce')
        players['age'] = players['birth_date'].apply(lambda x: datetime.now().year - x.year if pd.notnull(x) else None)

        # Merge på player_id
        df = pd.merge(players, metrics, on='player_id', how='left')
        # Merge - behold ALLE spillere, også dem uden metrics
        df = pd.merge(players, metrics, on='player_id', how='left')
        return df
    

    st.title("🔍 Information over spillere")
    data = fetch_data()

    # Kategorier
    def categorize_age(age):
        if age is None: return None
        if age < 23:
            return "Emerging"
        elif age < 27:
            return "Pre-peak"
        elif age < 31:
            return "Peak"
        else:
            return "Post-peak"

    def categorize_rating(r):
        if r is None: return None
        if r >= 75:
            return "Post-peak"
        elif r >= 70:
            return "Peak"
        elif r >= 65:
            return "Pre-peak"
        elif r >= 60:
            return "Emerging"
        else:
            return "Low"

    data['age_category'] = data['age'].apply(categorize_age)
    data['rating_category'] = data['rating'].apply(categorize_rating)

    # Sidebar filters
    st.sidebar.header("Filtre")
    search_name = st.sidebar.text_input("🔎 Søg efter spillerens navn:")
    selected_country = st.sidebar.selectbox("Vælg land:", ["Alle"] + sorted(data['nationality1'].dropna().unique()))
    selected_team = st.sidebar.selectbox("Vælg klub:", ["Alle"] + sorted(data['parent_team'].dropna().unique()))
    min_xt = st.sidebar.slider("Min. transferværdi (xTV) i mio. €", 0, 100, 0, 1)
    min_rating = st.sidebar.slider("Rating minimum", 0, 100, 0, 1)
    selected_age_cat = st.sidebar.selectbox("Alderskategori", ["Alle", "Emerging", "Pre-peak", "Peak", "Post-peak"])
    selected_rating_cat = st.sidebar.selectbox("Ratingkategori", ["Alle", "Emerging", "Pre-peak", "Peak", "Post-peak"])

    # Debug info
    st.sidebar.markdown("### ℹ️ Debug info")
    st.sidebar.write(f"Alle spillere i database: {len(data)}")

    if st.sidebar.button("🔄 Nulstil filtre"):
        st.rerun()

    # Filtrering
    filtered_data = data.copy()
    if search_name:
        filtered_data = filtered_data[filtered_data['player_name'].str.contains(search_name, case=False, na=False)]
    if selected_country != "Alle":
        filtered_data = filtered_data[filtered_data['nationality1'] == selected_country]
    if selected_team != "Alle":
        filtered_data = filtered_data[filtered_data['parent_team'] == selected_team]

    # Tillad spillere med NaN i rating/xTV at blive vist
    filtered_data = filtered_data[
        (filtered_data['rating'].isna()) | (filtered_data['rating'] >= min_rating)
    ]
    filtered_data = filtered_data[
        (filtered_data['xTV'].isna()) | (filtered_data['xTV'] >= min_xt)
    ]
    if selected_age_cat != "Alle":
        filtered_data = filtered_data[filtered_data['age_category'] == selected_age_cat]
    if selected_rating_cat != "Alle":
        filtered_data = filtered_data[filtered_data['rating_category'] == selected_rating_cat]

    st.sidebar.write(f"Efter filtrering: {len(filtered_data)}")
    st.write(f"Viser **{len(filtered_data)}** spillere ud af {len(data)}")

    # 📋 Tabelvisning
    st.subheader("📋 Information over spillere")
    if filtered_data.empty:
        st.warning("Ingen spillere matcher dine søgekriterier.")
    else:
        st.dataframe(
            filtered_data[
                ["tr_id", "competition_id", "player_name", "birth_date", "first_position",
                 "nationality1", "nationality2", "parent_team", "xTV", "rating"]
            ],
            use_container_width=True
        )


        st.subheader("📌 Nationalitetsfordeling")
        nat_count = filtered_data['nationality1'].value_counts().reset_index()
        nat_count.columns = ['Nationality', 'Count']
        st.plotly_chart(px.bar(nat_count, x='Nationality', y='Count'))

        st.subheader("⚽ Fordeling af positioner")
        pos_count = filtered_data['first_position'].value_counts()
        st.plotly_chart(px.pie(names=pos_count.index, values=pos_count.values))

        st.subheader("🎂 Aldersfordeling")
        st.plotly_chart(px.histogram(filtered_data, x='age', nbins=20))

        st.subheader("🏟️ Spillere pr. klub")
        club_counts = filtered_data['parent_team'].value_counts().head(10).reset_index()
        club_counts.columns = ['Team', 'Player Count']
        st.plotly_chart(px.bar(club_counts, x='Team', y='Player Count'))

        st.subheader("🌍 Heatmap: Position vs. Nationalitet")
        heat_data = filtered_data.groupby(['first_position', 'nationality1']).size().reset_index(name='count')
        st.plotly_chart(px.density_heatmap(heat_data, x="nationality1", y="first_position", z="count"))

        st.subheader("🎂 Gennemsnitsalder pr. position")
        age_pos = filtered_data.groupby("first_position")["age"].mean().reset_index()
        st.plotly_chart(px.bar(age_pos, x="first_position", y="age"))

        st.subheader("📆 Fødselsår")
        filtered_data["birth_year"] = filtered_data["birth_date"].dt.year
        st.plotly_chart(px.histogram(filtered_data, x="birth_year", nbins=20))

        agencies_df = pd.read_sql("SELECT * FROM agencies", engine)
        player_agency_df = pd.read_sql("SELECT * FROM player_agency", engine)
        merged_data = pd.merge(player_agency_df, agencies_df, on='agency_id')
        agency_count = merged_data.groupby('agency_name').size().reset_index(name='player_count')
        st.subheader("🤝 Spillere per agentur")
        st.plotly_chart(px.bar(agency_count, x='agency_name', y='player_count'))
