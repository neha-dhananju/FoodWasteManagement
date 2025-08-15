import streamlit as st
import time
from db import add_provider, provider_exists,provider_id_exists # import your backend functions

st.title("Add New Provider")

with st.form("receiver_form"):
    receiver_id = st.text_input("Receiver ID")
    name = st.text_input("Name")
    receiver_type = st.text_input("Type")
    city = st.text_input("City")
    contact = st.text_input("Contact Number")

    submit = st.form_submit_button("Submit")

    if submit:
        if not receiver_id or not name or not receiver_type or not city or not contact:
            st.error("Please fill all required fields!")
        elif provider_id_exists(receiver_id):
            st.error("Provider ID already taken. Please choose another ID.")
        elif provider_exists(name, receiver_type, city, contact):
            st.error("User already exists!")
        else:
            add_provider(receiver_id, name, receiver_type, city, contact)
            st.success(f"Provider '{name}' added successfully!")

            time.sleep(3)  # Show success message for 3 seconds

            # Clear form fields
            st.session_state.provider_id = ""
            st.session_state.name = ""
            st.session_state.provider_type = ""
            st.session_state.address = ""
            st.session_state.city = ""
            st.session_state.contact = ""

            st.rerun()  
