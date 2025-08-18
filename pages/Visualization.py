import streamlit as st
import queries  # the backend file you created
import matplotlib.pyplot as plt

st.set_page_config(page_title="Food Insights", layout="wide")

st.title("📊 Food Management Analytics")

# Dropdown for selecting question
question = st.selectbox(
    "Choose an analysis question:",
    [
        "How many food providers and receivers are there in each city?",
        "Which type of food provider contributes the most food?",
        "What is the contact information of food providers in a specific city?",
        "Which receivers have claimed the most food?",
        "What is the total quantity of food available from all providers?",
        "Which city has the highest number of food listings?",
        "What are the most commonly available food types?",
        "How many food claims have been made for each food item?",
        "Which provider has had the highest number of successful food claims?",
        "What percentage of food claims are completed vs. pending vs. canceled?",
        "What is the average quantity of food claimed per receiver?",
        "Which meal type is claimed the most?",
        "What is the total quantity of food donated by each provider?",
    ]
)

# Handle each question
if question == "How many food providers and receivers are there in each city?":
    df = queries.food_providers_receivers_by_city()
    st.bar_chart(df.set_index("city"))

elif question == "Which type of food provider contributes the most food?":
    df = queries.top_food_provider_type()
    st.bar_chart(df.set_index("type"))

elif question == "What is the contact information of food providers in a specific city?":
    city = st.text_input("Enter city:")
    if city:
        df = queries.contact_info_by_city(city)
        st.dataframe(df)

# … Similarly for the rest of the 12
