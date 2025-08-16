import streamlit as st
import pandas as pd
from db import get_claim_by_id, delete_claim

st.title("🗑️ Delete Claim")

# Step 1: Receiver enters Claim ID & Receiver ID
claim_id = st.text_input("Enter Claim ID")
receiver_id = st.text_input("Enter Receiver ID")

if st.button("🔍 Search Claim"):
    if not claim_id or not receiver_id:
        st.error("⚠️ Please provide both Claim ID and Receiver ID.")
    else:
        claim = get_claim_by_id(claim_id, receiver_id)
        if claim:
            df = pd.DataFrame([claim])
            st.dataframe(df, use_container_width=True)

            if st.button("🗑️ Confirm Delete"):
                delete_claim(claim_id, receiver_id)
                st.success(f"Claim ID {claim_id} deleted successfully.")

        else:
            st.error("❌ Claim not found or does not belong to this Receiver.")
