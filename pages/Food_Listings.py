import streamlit as st

st.title("Food Listing Page")

# Layout for 4 buttons
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

with col1:
    if st.button("Add Food"):
        st.switch_page("pages/Add_Food.py")

with col2:
    if st.button("Update Food"):
        st.switch_page("pages/Update_Food.py")

with col3:
    if st.button("View Food"):
        st.switch_page("pages/View_Food.py")

with col4:
    if st.button("Delete Food"):
        st.switch_page("pages/Delete_Food.py")
