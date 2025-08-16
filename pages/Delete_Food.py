import streamlit as st
from db import get_food, delete_food

st.title("🗑️ Delete Food Listing")

# Input form for Provider ID and Food ID
provider_id = st.text_input("Enter Provider ID")
food_id = st.text_input("Enter Food ID")

if st.button("Fetch Food Details"):
    if provider_id and food_id:
        food = get_food(provider_id, food_id)
        if food:
            st.success("Food item found! Please confirm deletion below.")
            
            # Show details in a table
            st.table({
                "Food ID": [food["Food_ID"]],
                "Food Name": [food["Food_Name"]],
                "Quantity": [food["Quantity"]],
                "Expiry Date": [food["Expiry_Date"]],
                "Provider ID": [food["Provider_ID"]],
                "Provider Type": [food["Provider_Type"]],
                "Location": [food["Location"]],
                "Food Type": [food["Food_Type"]],
                "Meal Type": [food["Meal_Type"]],
            })

            # Confirmation step
            confirm = st.radio(
                "Are you sure you want to delete this food item?",
                ("No", "Yes")
            )

            if confirm == "Yes":
                if st.button("✅ Confirm Delete"):
                    delete_food(provider_id, food_id)
                    st.success("✅ Food item deleted successfully!")
        else:
            st.error("❌ No food item found with this Provider ID and Food ID.")
    else:
        st.warning("Please enter both Provider ID and Food ID.")
