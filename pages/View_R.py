import streamlit as st
import pandas as pd
from db import get_table  # to fetch provider data

st.title("Existing Provider Details")

# Fetch all providers from database
receivers_df = get_table("receivers")

# Check if there are providers
if receivers_df.empty:
    st.warning("No receviers found in the database.")
else:
    # Dropdown with Provider IDs
    receivers_ids = receivers_df["Receiver_ID"].tolist()
    selected_id = st.selectbox("Select Provider ID", receivers_ids)

    # Button to fetch details
    if st.button("View Details"):
        receiver = receivers_df[receivers_df["Provider_ID"] == selected_id].iloc[0]

        # Display provider details
        st.subheader("Provider Details")
        st.write(f"**Name:** {receiver['Name']}")
        st.write(f"**Type:** {receiver['Type']}")
        st.write(f"**City:** {receiver['City']}")
        st.write(f"**Contact:** {receiver['Contact']}")

        
