import streamlit as st
from utils import hide_sidebar
hide_sidebar()


st.title("Reciever Page")

# CSS for plain white buttons
st.markdown("""
    <style>
    .plain-button {
        background-color: white;
        color: black;
        border: 2px solid black;
        padding: 15px 30px;
        font-size: 16px;
        font-weight: bold;
        cursor: pointer;
        margin: 10px;
        border-radius: 5px;
        transition: background-color 0.2s ease, transform 0.2s ease;
    }
    .plain-button:hover {
        background-color: #f0f0f0;
        transform: scale(1.05);
    }
    .button-container {
        display: flex;
        justify-content: center;
        gap: 30px;
        margin-top: 50px;
    }
    </style>
""", unsafe_allow_html=True)

# Streamlit-native buttons for navigation
col1, col2 = st.columns(2)

with col1:
    if st.button("New Reciever"):
        st.switch_page("pages/New_Reciever.py")  # Navigates to New_Provider.py

with col2:
    if st.button("Existing Reciever"):
        st.switch_page("pages/Existing_Receiver.py")  # Optional: separate page
