# main.py
import streamlit as st

# Importer dine sider
from streamlit_app import (
    Front_page,
    Filter_and_Overview,
    Rating_Groups,
    playerMetricsBelgic,
    danishplayer,
    filteringPlayersbyposition
)

# Sidebar navigation
st.sidebar.title("Navigering")
sidevalg = st.sidebar.radio(
    "Gå til:",
    (
        "🏠 Forside",
        "🔍 Filtrering og Oversigt",
        "⭐ Rating-grupper",
        "📊 Belgiske spiller metrics",
        "🏳️ Danske spiller statistik",
        "🧃 Alle spillerfilter"
    )
)

# Routing
if sidevalg == "🏠 Forside":
    Front_page.run()
elif sidevalg == "🔍 Filtrering og Oversigt":
    Filter_and_Overview.run()
elif sidevalg == "⭐ Rating-grupper":
    Rating_Groups.run()
elif sidevalg == "📊 Belgiske spiller metrics":
    playerMetricsBelgic.run()
elif sidevalg == "🏳️ Danske spiller statistik":
    danishplayer.run()
elif sidevalg == "🧃 Alle spillerfilter":
    filteringPlayersbyposition.run()

