import streamlit as st
from utils import hide_sidebar
hide_sidebar()

st.title("Claims Page")

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
col3, col4 = st.columns(2)

with col1:
    if st.button("Want to Claim"):
        st.switch_page("/Users/nehadhananju/Desktop/FoodWasteManagement/pages/Add_claim.py")

with col2:
    if st.button("Update"):
        st.switch_page("/Users/nehadhananju/Desktop/FoodWasteManagement/pages/Update_claim.py")

with col3:
    if st.button("Delete"):
        st.switch_page("/Users/nehadhananju/Desktop/FoodWasteManagement/pages/Delete_claim.py")

with col4:
    if st.button("View"):
        st.switch_page("/Users/nehadhananju/Desktop/FoodWasteManagement/pages/View_claim.py")
