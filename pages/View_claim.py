import streamlit as st
import pandas as pd
from db import get_all_claims  # function in db.py

st.title("View Claims")

try:
    claims = get_all_claims()
    if claims.empty:
        st.info("No claims found.")
    else:
        st.dataframe(claims, use_container_width=True)
except Exception as e:
    st.error(f"Error loading claims: {e}")
