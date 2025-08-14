import streamlit as st
from db import get_table, add_provider, update_provider, delete_provider

st.set_page_config(page_title="Food Donation Management", layout="wide")
st.title("🍽 Food Donation Management System")

menu = ["View Data", "Add Provider", "Update Provider", "Delete Provider", "Analysis"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "View Data":
    st.subheader("Providers Table")
    st.dataframe(get_table("providers"))

    st.subheader("Receivers Table")
    st.dataframe(get_table("receivers"))

    st.subheader("Food Listings Table")
    st.dataframe(get_table("food_listings"))

    st.subheader("Claims Table")
    st.dataframe(get_table("claims"))

elif choice == "Add Provider":
    st.subheader("Add New Provider")
    pid = st.number_input("Provider ID", min_value=1)
    name = st.text_input("Name")
    type_ = st.text_input("Type")
    address = st.text_input("Address")
    city = st.text_input("City")
    contact = st.text_input("Contact")

    if st.button("Add Provider"):
        add_provider(pid, name, type_, address, city, contact)
        st.success(f"Provider {name} added successfully!")

elif choice == "Update Provider":
    st.subheader("Update Provider Details")
    pid = st.number_input("Provider ID to Update", min_value=1)
    city = st.text_input("New City")
    contact = st.text_input("New Contact")

    if st.button("Update"):
        update_provider(pid, city, contact)
        st.success(f"Provider {pid} updated successfully!")

elif choice == "Delete Provider":
    st.subheader("Delete Provider")
    pid = st.number_input("Provider ID to Delete", min_value=1)

    if st.button("Delete"):
        delete_provider(pid)
        st.success(f"Provider {pid} deleted successfully!")

elif choice == "Analysis":
    st.subheader("📊 Analysis Dashboard")
    df_food = get_table("food_listings")
    st.write("### Food Quantity by Type")
    food_type_counts = df_food.groupby("Food_Type")["Quantity"].sum().reset_index()
    st.bar_chart(food_type_counts, x="Food_Type", y="Quantity")

    st.write("### Providers by City")
    df_providers = get_table("providers")
    city_counts = df_providers["City"].value_counts().reset_index()
    city_counts.columns = ["City", "Count"]
    st.bar_chart(city_counts, x="City", y="Count")
