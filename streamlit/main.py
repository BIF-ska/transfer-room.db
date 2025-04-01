import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(page_title="Player Stats App", layout="wide")

with st.sidebar:
    selected = option_menu(
        menu_title="Navigation",
        options=["Home", "Danish Players", "Belgium Metrics", "Rating Groups", "Overview for all players"],
        icons=["house", "flag", "bar-chart", "layers", "grid"],
        menu_icon="cast",
        default_index=0,
    )

if selected == "Home":
    import home
    home.run()

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