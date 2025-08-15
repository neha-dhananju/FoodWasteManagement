import streamlit as st
from db import add_provider, provider_exists  # import your backend functions

st.title("Add New Provider")

with st.form("provider_form"):
    provider_id = st.text_input("Provider ID")
    name = st.text_input("Name")
    provider_type = st.text_input("Type")
    address = st.text_input("Address")
    city = st.text_input("City")
    contact = st.text_input("Contact Number")

    submit = st.form_submit_button("Submit")

    if submit:
        if not provider_id or not name:
            st.error("Please fill all required fields!")
        elif provider_exists(provider_id, name, provider_type, address, city, contact):
            st.error("User already exists!")
        else:
            add_provider(provider_id, name, provider_type, address, city, contact)
            st.success(f"Provider '{name}' added successfully!")
