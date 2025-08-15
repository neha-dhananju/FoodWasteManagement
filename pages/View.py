import streamlit as st
import pandas as pd
from db import get_table  # to fetch provider data

st.title("Existing Provider Details")

# Fetch all providers from database
providers_df = get_table("providers")

# Check if there are providers
if providers_df.empty:
    st.warning("No providers found in the database.")
else:
    # Dropdown with Provider IDs
    provider_ids = providers_df["Provider_ID"].tolist()
    selected_id = st.selectbox("Select Provider ID", provider_ids)

    # Button to fetch details
    if st.button("View Details"):
        provider = providers_df[providers_df["Provider_ID"] == selected_id].iloc[0]

        # Display provider details
        st.subheader("Provider Details")
        st.write(f"**Name:** {provider['Name']}")
        st.write(f"**Type:** {provider['Type']}")
        st.write(f"**Address:** {provider['Address']}")
        st.write(f"**City:** {provider['City']}")
        st.write(f"**Contact:** {provider['Contact']}")
