import streamlit as st
import db

st.set_page_config(page_title="Provider Dashboard", layout="wide")

if "logged_in_provider" not in st.session_state:
    st.error("⚠️ Please log in first!")
    st.stop()

provider_id = st.session_state["logged_in_provider"]

st.title("📊 Provider Dashboard")

if st.button("👀 View"):
    st.switch_page("pages/View_provider.py")

if st.button("✏️ Update"):
    st.switch_page("pages/Update_provider.py")

if st.button("🗑️ Delete"):
    st.switch_page("pages/Delete_provider.py")
