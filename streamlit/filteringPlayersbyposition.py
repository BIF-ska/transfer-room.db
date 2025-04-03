import streamlit as st
import pandas as pd
import os
from sqlalchemy import create_engine
from pathlib import Path
import sys
from dotenv import load_dotenv
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

def run():
    sys.path.append(str(Path(__file__).parents[1]))
    sys.path.append(str(Path(__file__).parents[0]))

    load_dotenv()
    engine = create_engine(os.getenv("DATABASE_URL"))

    @st.cache_data
    def load_data():
        return pd.read_sql("SELECT * FROM players", engine)

    data = load_data()

    # Convert birth_date to datetime and calculate age
    data['birth_date'] = pd.to_datetime(data['birth_date'], errors='coerce')
    data['age'] = data['birth_date'].apply(lambda x: datetime.now().year - x.year if pd.notnull(x) else None)

    # Sidebar filters
    st.sidebar.header("🔍 Filtre")

    # Nationality dropdown (with "Alle lande")
    nationalities = sorted(data['nationality1'].dropna().unique().tolist())
    nationalities.insert(0, "Alle lande")
    selected_nationality = st.sidebar.selectbox("🌍 Vælg nationalitet:", nationalities)

    # Age slider
    age_min, age_max = int(data['age'].min()), int(data['age'].max())
    selected_age = st.sidebar.slider("🎂 Alder", min_value=age_min, max_value=age_max, value=(age_min, age_max))

    # Rating slider
    rating_min, rating_max = int(data['rating'].min()), int(data['rating'].max())
    selected_rating = st.sidebar.slider("⭐ Rating", min_value=0, max_value=100, value=(rating_min, rating_max))

    # xTV slider
    xtv_min, xtv_max = int(data['xTV'].min()), int(data['xTV'].max())
    selected_xtv = st.sidebar.slider("💸 xTV", min_value=xtv_min, max_value=xtv_max, value=(xtv_min, xtv_max))

    # Position tabs
    positions = data['first_position'].dropna().unique().tolist()
    positions.sort()
    tabs = st.tabs(positions)

    for i, tab in enumerate(tabs):
        with tab:
            position = positions[i]
            df_filtered = data[data['first_position'] == position]

            # Apply filters
            if selected_nationality != "Alle lande":
                df_filtered = df_filtered[df_filtered['nationality1'] == selected_nationality]

            df_filtered = df_filtered[
                (df_filtered['age'] >= selected_age[0]) & (df_filtered['age'] <= selected_age[1]) &
                (df_filtered['rating'] >= selected_rating[0]) & (df_filtered['rating'] <= selected_rating[1]) &
                (df_filtered['xTV'] >= selected_xtv[0]) & (df_filtered['xTV'] <= selected_xtv[1])
            ]

            st.subheader(f"📌 Spillere i position: {position}")
            st.dataframe(df_filtered)

            # Plotly scatter plot
            if not df_filtered.empty:
                fig = px.scatter(
                    df_filtered,
                    x="rating",
                    y="xTV",
                    color="nationality1",
                    hover_data=["age", "rating", "xTV"],
                    title=f"📈 Rating vs xTV for {position}"
                )
                st.plotly_chart(fig, use_container_width=True)

                # Age vs Rating and Age vs xTV based on filtered data
                st.subheader("📊 Age vs Rating and Age vs xTV")

                data_grouped = df_filtered.groupby('age').agg({
                    'rating': 'mean',
                    'xTV': 'mean'
                }).reset_index()

                # Plot for Age vs Rating
                fig1 = go.Figure()
                fig1.add_trace(go.Scatter(
                    x=data_grouped['age'], 
                    y=data_grouped['rating'], 
                    mode='lines+markers', 
                    name='Rating',
                    line=dict(color='orange'),
                    marker=dict(size=8)  
                ))

                fig1.update_layout(
                    title="Age vs Rating",
                    xaxis_title="Age (years)",
                    yaxis_title="Rating",
                    showlegend=True,
                    hovermode="closest"
                )

                st.plotly_chart(fig1)

                # Plot for Age vs xTV
                fig2 = go.Figure()
                fig2.add_trace(go.Scatter(
                    x=data_grouped['age'], 
                    y=data_grouped['xTV'], 
                    mode='lines+markers', 
                    name='xTV (€)',
                    line=dict(color='blue'),
                    marker=dict(size=8)
                ))

                fig2.update_layout(
                    title="Age vs xTV",
                    xaxis_title="Age (years)",
                    yaxis_title="xTV (€)",
                    showlegend=True,
                    hovermode="closest"
                )

                st.plotly_chart(fig2)

            else:
                st.info("Ingen spillere matcher de valgte filtre for denne position.")
