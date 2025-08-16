import streamlit as st
from db import food_id_exists, add_food

st.title("Add Food")

# Form
with st.form("add_food_form"):
    food_id = st.text_input("Food ID")
    food_name = st.text_input("Food Name")
    quantity = st.number_input("Quantity", min_value=1)
    expiry_date = st.date_input("Expiry Date")

    provider_id = st.text_input("Provider ID")
    provider_type = st.text_input("Provider Type")
    location = st.text_input("Location")

    food_type = st.selectbox("Food Type", ["Vegetarian", "Non-Vegetarian", "Vegan", "Other"])
    meal_type = st.selectbox("Meal Type", ["Breakfast", "Lunch", "Dinner", "Snacks"])

    submitted = st.form_submit_button("Submit")

    if submitted:
        if food_id_exists(food_id):
            st.error("⚠️ Food ID already exists! Please use a different ID.")
        else:
            add_food(food_id, food_name, quantity, expiry_date, provider_id, provider_type, location, food_type, meal_type)
            st.success("✅ Food added successfully!")
