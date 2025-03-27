import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def run():
    st.title("🇩🇰 Danish Player Stats Explorer")

    # Upload or load local file
    uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx", "xls"])

    if uploaded_file is not None:
        # Load all sheets and merge
        excel_data = pd.read_excel(uploaded_file, sheet_name=None)
        df = pd.concat(excel_data.values(), ignore_index=True)
        st.success("File uploaded successfully.")
    else:
        default_path = r"C:\Users\ska\OneDrive - Brøndbyernes IF Fodbold\Dokumenter\GitHub\danish_players.xlsx"
        try:
            excel_data = pd.read_excel(default_path, sheet_name=None)
            df = pd.concat(excel_data.values(), ignore_index=True)
            st.info("Using default file from local path.")
        except FileNotFoundError:
            st.error("No file uploaded and default file not found.")
            st.stop()

    # Clean numeric columns
    df['Age_decimal'] = df['Age_decimal'].astype(str).str.replace(',', '.').astype(float)
    df['Rating'] = df['Rating'].astype(str).str.replace(',', '.').astype(float)

    # Sidebar filter: Age Group
    st.sidebar.header("Aldersgruppe Filter")
    age_groups = df['AgeGroup'].dropna().unique()
    selected_age_group = st.sidebar.multiselect("Vælg aldersgruppe:", list(age_groups), default=list(age_groups))

    # Filter by AgeGroup
    df = df[df['AgeGroup'].isin(selected_age_group)]

    # Unique positions from data
    positions = df['FirstPosition'].dropna().unique().tolist()
    tabs = st.tabs(positions)

    for i, tab in enumerate(tabs):
        with tab:
            selected_position = positions[i]
            df_pos = df[df['FirstPosition'] == selected_position]

            st.subheader(f"📌 Spillere i position: {selected_position}")
            st.dataframe(df_pos)

            if df_pos.empty:
                st.warning("Ingen spillere i denne kombination.")
                continue

            # Stats
            st.subheader("📊 Statistisk Oversigt")
            st.write(df_pos.describe())

            # Histogram
            st.subheader("📈 Ratingfordeling")
            fig, ax = plt.subplots()
            df_pos['Rating'].hist(bins=10, ax=ax)
            ax.set_xlabel("Rating")
            ax.set_ylabel("Antal spillere")
            st.pyplot(fig)

            # Boxplot
            st.subheader("📦 Aldersboxplot pr. Gruppe")
            fig2, ax2 = plt.subplots()
            try:
                df_pos.boxplot(column='Age_decimal', by='AgeGroup', ax=ax2)
                plt.title("")
                ax2.set_ylabel("Alder")
                st.pyplot(fig2)
            except:
                st.info("Ikke nok data til at vise boxplot.")
