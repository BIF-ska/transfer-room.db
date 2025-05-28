from bif_streamlit.layout_utils import StreamlitBIFStyles


def set_up_streamlit():
    st_style = StreamlitBIFStyles(app_name='Match Report')
    st_style.apply_bif_layout()
    st_style.add_sidebar_logo_and_header()
    st_style.wide_mode()