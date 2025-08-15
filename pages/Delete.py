import streamlit as st
from db import   get_table,delete_provider  # import your backend functions

st.title("Update Provider")
providers_df = get_table("providers")
if providers_df.empty:
    st.warning("No providers found in the database.")

else:

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
