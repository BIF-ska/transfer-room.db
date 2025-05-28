import streamlit as st
import pandas as pd
import os
from sqlalchemy import create_engine
from pathlib import Path
import sys 
from dotenv import load_dotenv
from datetime import datetime
import plotly.express as px

def run():
    sys.path.append(str(Path(__file__).parents[1]))
    sys.path.append(str(Path(__file__).parents[0]))

    load_dotenv()
    print("Loaded URL:", os.getenv("DATABASE_URL"))
    engine = create_engine(os.getenv("DATABASE_URL"))

    @st.cache_data
    def load_data():
        players = pd.read_sql("SELECT * FROM players", engine)
        metrics = pd.read_sql("SELECT * FROM player_metrics", engine)

        players['birth_date'] = pd.to_datetime(players['birth_date'], errors='coerce')
        players['age'] = players['birth_date'].apply(lambda x: datetime.now().year - x.year if pd.notnull(x) else None)

        df = players.merge(metrics, on="player_id", how="inner")
        df["contract_expiry"] = pd.to_datetime(df["contract_expiry"], errors="coerce")
        return df

    df = load_data()
    st.title("📊 Belgiske spiller-metrics")

    if "nationality1" in df.columns:
        df = df[df["nationality1"] == "Belgium"]

    # Check for positions
    positions = df['first_position'].dropna().unique().tolist()
    if not positions:
        st.warning("Ingen positionsdata fundet.")
        st.stop()

    tabs = st.tabs(positions)

    for i, tab in enumerate(tabs):
        with tab:
            selected_position = positions[i]
            df_pos = df[df['first_position'] == selected_position]

            st.subheader(f"📌 Spillere i position: {selected_position}")
            st.dataframe(df_pos)

            # Rating vs Potential
            if all(col in df_pos.columns for col in ["rating", "potential", "playing_style"]):
                fig = px.scatter(
                    df_pos.dropna(subset=["rating", "potential"]),
                    x="rating", y="potential",
                    hover_name="player_name",
                    color="playing_style",
                    title="Rating vs. Potential"
                )
                st.plotly_chart(fig)

            # Transfer Value Histogram
            if "xTV" in df_pos.columns:
                fig = px.histogram(df_pos.dropna(subset=["xTV"]), x="xTV", nbins=20,
                                   title="Fordeling af transferværdi (xTV)")
                st.plotly_chart(fig)

            # Contract Expiry Table
            if "contract_expiry" in df_pos.columns:
                st.subheader("📆 Spillere med kontraktudløb indenfor 1 år")
                expiring = df_pos[df_pos["contract_expiry"] < pd.Timestamp.now() + pd.DateOffset(years=1)]
                expected_cols = ["player_name", "contract_expiry", "xTV", "rating"]
                available_cols = [col for col in expected_cols if col in expiring.columns]

                if not expiring.empty and available_cols:
                    st.dataframe(expiring[available_cols])
                else:
                    st.info("Ingen spillere med kontraktudløb det næste år eller manglende kolonner.")

            # GBE Visualizations
            if "GBE_score" in df_pos.columns:
                if "GBE_result" in df_pos.columns:
                    fig = px.scatter(df_pos.dropna(subset=["GBE_score", "GBE_result"]),
                                     x="GBE_score", y="GBE_result",
                                     title="GBE Score vs. Result")
                    st.plotly_chart(fig)

                if "rating" in df_pos.columns:
                    fig = px.scatter(df_pos.dropna(subset=["GBE_score", "rating"]),
                                     x="GBE_score", y="rating", title="GBE Score vs. Rating")
                    st.plotly_chart(fig)

                if "xTV" in df_pos.columns:
                    fig = px.scatter(df_pos.dropna(subset=["GBE_score", "xTV"]),
                                     x="GBE_score", y="xTV", title="GBE Score vs. xTV")
                    st.plotly_chart(fig)

            # Rating vs xTV
            if all(col in df_pos.columns for col in ["rating", "xTV"]):
                fig = px.scatter(df_pos.dropna(subset=["rating", "xTV"]),
                                 x="rating", y="xTV", title="Rating vs. xTV")
                st.plotly_chart(fig)

            # Club bubble chart
            if "parent_team" in df_pos.columns:
                st.subheader("📊 Klub: Antal spillere vs. gennemsnitsalder")
                club_stats = df_pos.groupby("parent_team").agg({
                    "age": "mean",
                    "player_id": "count"
                }).reset_index()
                club_stats.columns = ["Team", "AvgAge", "PlayerCount"]

                fig = px.scatter(
                    club_stats,
                    x="AvgAge",
                    y="PlayerCount",
                    text="Team",
                    title="Klubber: Antal spillere vs. gennemsnitsalder",
                    size="PlayerCount",
                    color="AvgAge",
                    color_continuous_scale="Blues"
                )

                # 💡 Enhanced styling for readability
                fig.update_traces(textposition='top center', textfont=dict(color="white", size=12))
                fig.update_layout(
                    plot_bgcolor="#0E1117",
                    paper_bgcolor="#0E1117",
                    font_color="white",
                    title_font_color="gold",
                    legend_title_font_color="white"
                )

                st.plotly_chart(fig)
