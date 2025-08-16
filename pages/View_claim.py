import streamlit as st
import pandas as pd
from db import get_claims_by_receiver  # function in db.py

if "view_mode" not in st.session_state:
    st.session_state.view_mode = "search"
if "search_results" not in st.session_state:
    st.session_state.search_results = None


# --- Helper functions ---
def search_by_receiver(receiver_id):
    if not receiver_id.strip():
        st.error("Please enter a Receiver ID")
        return
    try:
        df = get_claims_by_receiver(receiver_id)
        st.session_state.search_results = df
        st.session_state.view_mode = "result"
    except Exception as e:
        st.error(f"Error fetching claims: {e}")


def go_back():
    st.session_state.view_mode = "search"
    st.session_state.search_results = None


# --- UI ---
st.title("View Claims")

if st.session_state.view_mode == "search":
    receiver_id = st.text_input("Enter Receiver ID")
    st.button("🔍 Get Claims", on_click=search_by_receiver, args=(receiver_id,))

elif st.session_state.view_mode == "result":
    st.subheader("Claims Details")
    if st.session_state.search_results is not None and not st.session_state.search_results.empty:
        st.dataframe(st.session_state.search_results, use_container_width=True)
    else:
        st.warning("No claims found for this Receiver ID.")
    st.button("🔙 Back to Search", on_click=go_back)