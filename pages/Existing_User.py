import streamlit as st
import pandas as pd
from db import get_table, provider_exists, update_provider, delete_provider

st.title("Existing Provider Management")

# Fetch all providers from database
providers_df = get_table("providers")
if providers_df.empty:
    st.warning("No providers found in the database.")
else:
    # Buttons to choose action
    col1, col2, col3 = st.columns(3)
    action = None
    with col1:
        if st.button("View User"):
            action = "view"
    with col2:
        if st.button("Update User"):
            action = "update"
    with col3:
        if st.button("Delete User"):
            action = "delete"

    # --- VIEW USER ---
    if action == "view":
        selected_id = st.selectbox("Select Provider ID", providers_df["Provider_ID"].tolist())
        if st.button("Show Details"):
            provider = providers_df[providers_df["Provider_ID"] == selected_id].iloc[0]
            st.subheader("Provider Details")
            st.write(f"**Name:** {provider['Name']}")
            st.write(f"**Type:** {provider['Type']}")
            st.write(f"**Address:** {provider['Address']}")
            st.write(f"**City:** {provider['City']}")
            st.write(f"**Contact:** {provider['Contact']}")

    # --- UPDATE USER ---
    if action == "update":
        selected_id = st.selectbox("Select Provider ID to Update", providers_df["Provider_ID"].tolist())
        provider = providers_df[providers_df["Provider_ID"] == selected_id].iloc[0]

        with st.form("update_form"):
            name = st.text_input("Name", provider["Name"])
            type_ = st.text_input("Type", provider["Type"])
            address = st.text_input("Address", provider["Address"])
            city = st.text_input("City", provider["City"])
            contact = st.text_input("Contact", provider["Contact"])

            submit = st.form_submit_button("Update")
            if submit:
                if not provider_exists(selected_id, provider["Name"], provider["Type"], provider["Address"], provider["City"], provider["Contact"]):
                    st.error("User does not exist!")
                else:
                    update_provider(selected_id, name, type_, address, city, contact)
                    st.success(f"Provider {selected_id} updated successfully!")

    # --- DELETE USER ---
    if action == "delete":
        selected_id = st.selectbox("Select Provider ID to Delete", providers_df["Provider_ID"].tolist())
        contact_input = st.text_input("Enter Contact Number to Confirm Deletion")

        if st.button("Delete"):
            # Check if ID and contact match
            provider = providers_df[providers_df["Provider_ID"] == selected_id].iloc[0]
            if provider["Contact"] != contact_input:
                st.error("Provider ID and Contact Number do not match!")
            else:
                delete_provider(selected_id)
                st.success(f"Provider {selected_id} deleted successfully!")
