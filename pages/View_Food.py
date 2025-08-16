import streamlit as st
import pandas as pd
from db import get_food_details, get_food_by_name

st.title("View Food Details")

# Session state
if "view_mode" not in st.session_state:
    st.session_state.view_mode = "search"
if "search_results" not in st.session_state:
    st.session_state.search_results = None

# --- Search functions ---
def search_by_id(food_id):
    if food_id:
        details = get_food_details(food_id)
        if details:
            st.session_state.search_results = pd.DataFrame([details])
            st.session_state.view_mode = "result"
        else:
            st.error("❌ Food ID not found.")
    else:
        st.warning("⚠️ Please enter a Food ID.")

def search_by_name(food_name):
    if food_name:
        results = get_food_by_name(food_name)
        if results:
            st.session_state.search_results = pd.DataFrame(results)
            st.session_state.view_mode = "result"
        else:
            st.error("❌ Food Name not found in the database.")
    else:
        st.warning("⚠️ Please enter a Food Name.")

def go_back():
    st.session_state.view_mode = "search"
    st.session_state.search_results = None

# --- UI ---
if st.session_state.view_mode == "search":
    search_type = st.radio("Search by:", ["Select...", "Food ID", "Food Name"], index=0)

    if search_type == "Food ID":
        food_id = st.text_input("Enter Food ID")
        st.button("🔍 Search", on_click=search_by_id, args=(food_id,))

    elif search_type == "Food Name":
        food_name = st.text_input("Enter Food Name")
        st.button("🔍 Search", on_click=search_by_name, args=(food_name,))

elif st.session_state.view_mode == "result":
    st.subheader("Food Details")
    st.dataframe(st.session_state.search_results, use_container_width=True)
    st.button("🔙 Back to Search", on_click=go_back)
