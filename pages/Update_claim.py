import streamlit as st
from db import update_claim_status  # you’ll write this in db.py

st.title("Update Claim Status")

# --- Input fields ---
claim_id = st.number_input("Enter Claim ID", min_value=1, step=1)
new_status = st.selectbox("Select New Status", ["Pending", "Approved", "Rejected", "Completed"])

# --- Submit button ---
if st.button("Update Status"):
    if not claim_id:
        st.error("Please provide Claim ID")
    else:
        try:
            result = update_claim_status(claim_id, new_status)
            if "Error" in result:
                st.error(result)
            else:
                st.success(result)
        except Exception as e:
            st.error(f"Something went wrong: {e}")
