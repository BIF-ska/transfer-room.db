from streamlit_app import (
    Front_page,
    Filter_and_Overview,
    Rating_Groups,
    playerMetricsBelgic,
    danishplayer,
    filteringPlayersbyposition,
    Player_Selector  # ny import
)

import streamlit as st


st.sidebar.title("Navigering")
sidevalg = st.sidebar.radio(
    "Gå til:",
    (
        "🏠 Forside",
        "🔍 Filtrering og Oversigt",
        "⭐ Rating-grupper",
        "📊 Belgiske spiller metrics",
        "🏳️ Danske spiller statistik",
        "🧃 Alle spillerfilter",
        "🔎 Vælg spiller"  # ny valgmulighed
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
elif sidevalg == "🔎 Vælg spiller":
    Player_Selector.run()
