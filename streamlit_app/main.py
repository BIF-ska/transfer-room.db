
import streamlit as st
from streamlit_option_menu import option_menu
from __init__ import set_up_streamlit

set_up_streamlit()






with st.sidebar:
    selected = option_menu(
        menu_title="Navigation",
        options=["Home", "Danish Players", "Belgium Metrics", "Rating Groups", "Overview for all players", "Alle Spillerfilter"],
        icons=["house", "flag", "bar-chart", "layers", "grid", "funnel"],
        menu_icon="cast",
        default_index=0,
    )

if selected == "Home":
    import Front_page
    Front_page.run()

elif selected == "Danish Players":
    import danishplayer 
    danishplayer.run()

elif selected == "Belgium Metrics":
    import playerMetricsBelgic
    playerMetricsBelgic.run()

elif selected == "Rating Groups":
    import Rating_Groups
    Rating_Groups.run()

elif selected == "Overview for all players":
    import Filter_and_Overview 
    Filter_and_Overview.run()

elif selected == "Alle Spillerfilter":
    import filteringPlayersbyposition 
    filteringPlayersbyposition.run()
