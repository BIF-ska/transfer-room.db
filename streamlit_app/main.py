import streamlit as st

# Importér moduler i samme mappe
import Front_page
import Filter_and_Overview
import Rating_Groups
import playerMetricsBelgic
import danishplayer
import filteringPlayersbyposition
import Player_Selector

# Sidebar navigation
st.sidebar.title("Navigering")
sidevalg = st.sidebar.radio(
    "Gå til:",
    (
        "🏠 Forside",
        "🔍 Information over spillere",
        "⭐ Rating-grupper",
        "📊 Belgiske spiller metrics",
        "🏳️ Danske spiller statistik",
        "🧃 Alle spillerfilter",
        "🔎 Vælg spiller"
    )
)

# Routing
if sidevalg == "🏠 Forside":
    Front_page.run()
elif sidevalg == "🔍 Information over spillere":
    Filter_and_Overview.run()
elif sidevalg == "⭐ Rating-grupper":
    Rating_Groups.run()
elif sidevalg == "📊 Belgiske spiller metrics":
    playerMetricsBelgic.run()
elif sidevalg == "🏳️ Danske spiller statistik":
    danishplayer.run()
elif sidevalg == "🧃 Alle spillerfilter":
    filteringPlayersbyposition.run()
elif sidevalg == "🔎 Vælg spiller":
    Player_Selector.run()
