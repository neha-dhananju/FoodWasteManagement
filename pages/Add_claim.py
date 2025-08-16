import streamlit as st
from db import add_claim  # your function with receiver validation + quantity handling

st.title("Add a Claim")

# --- Input fields ---
receiver_id = st.text_input("Enter Receiver ID")
food_id = st.text_input("Enter Food ID")
quantity = st.number_input("Enter Quantity", min_value=1, step=1)

# --- Submit button ---
if st.button("Submit Claim"):
    if not receiver_id or not food_id:
        st.error("Please provide both Receiver ID and Food ID.")
    else:
        try:
            # Call the DB function
            result = add_claim(receiver_id, food_id, quantity)
            if "Error" in result:
                st.error(result)
            else:
                st.success(result)
        except Exception as e:
            st.error(f"Something went wrong: {e}")
