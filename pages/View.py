import streamlit as st
import pandas as pd
from db import get_table  # to fetch provider, food, and claims data

st.title("Existing Provider Details")

# Fetch all tables
providers_df = get_table("providers")
foods_df = get_table("food_listings")   # <-- assumes you have this table
claims_df = get_table("claims")

if providers_df.empty:
    st.warning("No providers found in the database.")
else:
    provider_ids = providers_df["Provider_ID"].tolist()
    selected_id = st.selectbox("Select Provider ID", provider_ids)

    if st.button("View Details"):
        provider = providers_df[providers_df["Provider_ID"] == selected_id].iloc[0]

        st.subheader("Provider Details")
        st.write(f"**Name:** {provider['Name']}")
        st.write(f"**Type:** {provider['Type']}")
        st.write(f"**Address:** {provider['Address']}")
        st.write(f"**City:** {provider['City']}")
        st.write(f"**Contact:** {provider['Contact']}")

        # --- Step 1: Get food items by this provider
        provider_foods = foods_df[foods_df["Provider_ID"] == selected_id]

        # --- Step 2: Get claims on those foods
        provider_claims = claims_df[claims_df["Food_ID"].isin(provider_foods["Food_ID"])]

        st.subheader("Claims Information")
        if provider_claims.empty:
            st.info("No claims made yet for this provider’s food.")
        else:
            # Merge with receivers table if you want receiver details
            receivers_df = get_table("receivers")
            merged = provider_claims.merge(receivers_df, left_on="Receiver_ID", right_on="Receiver_ID", how="left")

            # Show summary
            st.write(f"**Total Food Claimed:** {len(provider_claims)}")
            st.dataframe(
                merged[["Claim_ID", "Food_ID", "Receiver_ID", "Name", "Status", "Timestamp"]],
                use_container_width=True
            )
