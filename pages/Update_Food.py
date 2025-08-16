import streamlit as st
from db import get_all_foods,get_food, update_food
from utils import hide_sidebar

hide_sidebar()
st.title("Update Food")

provider_id = st.text_input("Enter Provider ID")
food_id = st.text_input("Enter Food ID")

if st.button("Fetch Food Details"):
    if provider_id and food_id:
        food = get_food(provider_id, food_id)

        if food:  # ✅ Found match
            st.success("Food found! Update details below 👇")

            # Show dropdown of all foods under this provider
            all_foods = get_all_foods(provider_id)
            food_options = {f"{f['Food_ID']} - {f['Food_Name']}": f['Food_ID'] for f in all_foods}
            selected_food = st.selectbox("Other Food Items for this Provider", options=list(food_options.keys()))

            # If dropdown changes, fetch that food
            selected_food_id = food_options[selected_food]
            if selected_food_id != food_id:
                food = get_food(provider_id, selected_food_id)
                food_id = selected_food_id  # update current food id

            # Editable form
        
            food_name = st.text_input("Food Name", value=food["Food_Name"])
            quantity = st.number_input("Quantity", min_value=1, value=food["Quantity"])
            expiry_date = st.date_input("Expiry Date", value=food["Expiry_Date"])
            provider_type = st.text_input("Provider Type", value=food["Provider_Type"])
            location = st.text_input("Location", value=food["Location"])
            food_type = st.text_input("Food Type", value=food["Food_Type"])
            meal_type = st.text_input("Meal Type", value=food["Meal_Type"])

            if st.button("Update Food"):
                update_food(food_id, provider_id,food_name,quantity,expiry_date,provider_type,location,food_type,meal_type)
                st.success(f"✅ Food ID {food_id} updated successfully!")

        else:
            st.error("❌ No food found for given Provider ID and Food ID")
    else:
        st.warning("Please enter both Provider ID and Food ID")