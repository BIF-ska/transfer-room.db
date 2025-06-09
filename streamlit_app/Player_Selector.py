import streamlit as st
import pandas as pd
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"))

@st.cache_data
def get_all_players():
    query = """
    SELECT 
        tr_id, competition_id, player_id, player_name, birth_date, 
        first_position, nationality1, nationality2, parent_team
    FROM players
    """
    df = pd.read_sql(query, engine)
    df.dropna(subset=['player_name'], inplace=True)
    return df

def run():
    st.title("🔎 Spillervælger og komplet oversigt")

    df = get_all_players()

    # 🎯 Vælg én spiller
    st.subheader("🎯 Søg og vælg en spiller")
    selected_player = st.selectbox(
        "Søg spiller ({} tilgængelige)".format(len(df)),
        options=df['player_name'].sort_values().unique()
    )

    # Vis detaljer for den valgte spiller
    player_row = df[df['player_name'] == selected_player]
    st.success(f"Du har valgt: {selected_player}")

    st.subheader("📄 Spillerinformation")
    st.write(player_row.transpose())

    # 📋 Komplet tabel med pagination
    st.subheader("📋 Se alle spillere (med pagination)")
    per_page = 100
    total_pages = len(df) // per_page + (1 if len(df) % per_page else 0)
    page = st.number_input("Vælg side", min_value=1, max_value=total_pages, value=1, step=1)

    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    paged_df = df.iloc[start_idx:end_idx]

    st.write(f"Viser spillere {start_idx + 1} til {min(end_idx, len(df))} af {len(df)}")
    st.dataframe(paged_df, use_container_width=True)

    # 💾 Download-knap
    st.subheader("📥 Download alle spillere som CSV")
    csv = df.to_csv(index=False)
    st.download_button("Download CSV", csv, "alle_spillere.csv", "text/csv")
