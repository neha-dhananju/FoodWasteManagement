import streamlit as st
from db import   get_table,delete_receiver  # import your backend functions

st.title("Update Provider")
receiver_df = get_table("receivers")
if receiver_df.empty:
    st.warning("No providers found in the database.")

else:

    selected_id = st.selectbox("Select Provider ID to Delete", receiver_df["Receiver_ID"].tolist())
    contact_input = st.text_input("Enter Contact Number to Confirm Deletion")

    if st.button("Delete"):
            # Check if ID and contact match
        receiver = receiver_df[receiver_df["Provider_ID"] == selected_id].iloc[0]
        if receiver["Contact"] != contact_input:
            st.error("Provider ID and Contact Number do not match!")
        else:
            delete_receiver(selected_id)
            st.success(f"Receiver {selected_id} deleted successfully!")
