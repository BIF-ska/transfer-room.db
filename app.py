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
st.title("Database Viewer over spillere") 
 
if st.button("Load Data"):
    data = fetch_data()
    st.dataframe(data)  # Display the data in an interactive table
 

# Streamlit UI
st.title("🎯 Spillere: Interaktiv Visualisering")

data = fetch_data()

# ➤ SIDEBAR: FILTRE
st.sidebar.header("🔍 Filtre")

# Søgning på navn
search_name = st.sidebar.text_input("🔎 Søg efter spillerens navn:")

# Land og klub filtre
selected_country = st.sidebar.selectbox("Vælg land (nationality1):", ["Alle"] + sorted(data['nationality1'].dropna().unique()))
selected_team = st.sidebar.selectbox("Vælg klub (parent_team):", ["Alle"] + sorted(data['parent_team'].dropna().unique()))

# ➤ Filtrering
filtered_data = data.copy()

if search_name:
    filtered_data = filtered_data[filtered_data['player_name'].str.contains(search_name, case=False, na=False)]

if selected_country != "Alle":
    filtered_data = filtered_data[filtered_data['nationality1'] == selected_country]

if selected_team != "Alle":
    filtered_data = filtered_data[filtered_data['parent_team'] == selected_team]

st.write(f"Viser **{len(filtered_data)}** spillere ud af {len(data)}")

# ➤ VISUALISERINGER

# Nationalitet
st.subheader("📌 Nationalitetsfordeling")
nat_count = filtered_data['nationality1'].value_counts().reset_index()
nat_count.columns = ['Nationality', 'Count']
fig1 = px.bar(nat_count, x='Nationality', y='Count', title="Antal spillere pr. nationalitet")
st.plotly_chart(fig1)

# Positioner
st.subheader("⚽ Fordeling af positioner")
pos_count = filtered_data['first_position'].value_counts()
fig2 = px.pie(names=pos_count.index, values=pos_count.values, title='Positioner fordelt')
st.plotly_chart(fig2)

# Alder
st.subheader("🎂 Aldersfordeling")
fig3 = px.histogram(filtered_data, x='age', nbins=20, title='Aldersfordeling af spillere')
st.plotly_chart(fig3)

# Klub
st.subheader("🏟️ Spillere pr. klub")
club_counts = filtered_data['parent_team'].value_counts().head(10).reset_index()
club_counts.columns = ['Team', 'Player Count']
fig4 = px.bar(club_counts, x='Team', y='Player Count', title='Top 10 klubber med flest spillere')
st.plotly_chart(fig4)

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


st.subheader("🎂 Gennemsnitsalder pr. position")
age_pos = filtered_data.groupby("first_position")["age"].mean().reset_index()
fig_age_pos = px.bar(age_pos, x="first_position", y="age", title="Gennemsnitsalder pr. position")
st.plotly_chart(fig_age_pos)

st.subheader("📆 Fødselsår")
filtered_data["birth_year"] = filtered_data["birth_date"].dt.year
fig_birth = px.histogram(filtered_data, x="birth_year", nbins=20, title="Fødselsår for spillere")
st.plotly_chart(fig_birth)


st.subheader("📊 Klub: Antal spillere vs. gennemsnitsalder")
club_stats = filtered_data.groupby("parent_team").agg({"age": "mean", "player_id": "count"}).reset_index()
club_stats.columns = ["Team", "AvgAge", "PlayerCount"]
fig_scatter = px.scatter(club_stats, x="AvgAge", y="PlayerCount", text="Team",
                         title="Klubber: Antal spillere vs. gennemsnitsalder",
                         size="PlayerCount", color="AvgAge")
st.plotly_chart(fig_scatter)

st.subheader("📊 Rating vs. Potential")

# Husk at merge player_metrics med players vha. player_id
metrics = pd.read_sql("SELECT * FROM player_metrics", engine)
players = pd.read_sql("SELECT * FROM players", engine)
df = players.merge(metrics, on="player_id")

fig = px.scatter(
    df.dropna(subset=["rating", "potential"]),
    x="rating",
    y="potential",
    hover_name="player_name",
    color="playing_style",
    title="Rating vs. Potential (spillere med playing_style)"
)
st.plotly_chart(fig)

st.subheader("💰 Fordeling af Transferværdi (xTV)")

fig = px.histogram(df, x="xTV", nbins=20, title="Fordeling af xTV")
st.plotly_chart(fig)

st.subheader("📆 Spillere med kontraktudløb indenfor 1 år")

df["contract_expiry"] = pd.to_datetime(df["contract_expiry"], errors="coerce")
upcoming_expiry = df[df["contract_expiry"] < pd.Timestamp.now() + pd.DateOffset(years=1)]

st.dataframe(upcoming_expiry[["player_name", "contract_expiry", "xTV", "rating"]])

st.subheader("📊 GBE Score vs. GBE Result"
             ) 
fig = px.scatter(df.dropna(subset=["GBE_score", "GBE_result"]), x="GBE_score", y="GBE_result", title="GBE Score vs. Result")
st.plotly_chart(fig)

st.subheader("📊 GBE Score vs. Rating"
             )
fig = px.scatter(df.dropna(subset=["GBE_score", "rating"]), x="GBE_score", y="rating", title="GBE Score vs. Rating")
st.plotly_chart(fig)

st.subheader("📊 GBE Score vs. xTV"
                )
fig = px.scatter(df.dropna(subset=["GBE_score", "xTV"]), x="GBE_score", y="xTV", title="GBE Score vs. xTV")
st.plotly_chart(fig)

st.subheader("📊 Rating vs. xTV"
                )
fig = px.scatter(df.dropna(subset=["rating", "xTV"]), x="rating", y="xTV", title="Rating vs. xTV")
st.plotly_chart(fig)



