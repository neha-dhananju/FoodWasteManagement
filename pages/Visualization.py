import streamlit as st
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt
import altair as alt
from queries import (
    get_providers_and_receivers_per_city,
    get_top_contributing_provider_type,
    get_providers_contact_by_city,
    get_top_receivers_by_claims,
    get_total_available_food,
    get_city_with_highest_food_listings,
    get_most_common_food_types,
    get_food_claims_per_item,
    get_top_successful_provider,
    get_claim_status_percentage,
    get_avg_claimed_quantity_per_receiver,
    get_most_claimed_meal_type,
    get_total_donated_by_provider,
)
from utils import hide_sidebar

# ---- Page Config ----
st.set_page_config(page_title="Food Management System", layout="wide")
hide_sidebar()

# ---- MySQL Connection ----
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root1234",  # replace with your DB password
        database="food_donation"
    )

# ---- Query Mapping ----
query_mapping = {
    "Food providers and receivers in each city": get_providers_and_receivers_per_city,
    "Provider type contributing the most food": get_top_contributing_provider_type,
    "Provider contacts in a specific city": get_providers_contact_by_city,
    "Receivers with the most food claims": get_top_receivers_by_claims,
    "Total quantity of food available": get_total_available_food,
    "City with the highest number of food listings": get_city_with_highest_food_listings,
    "Most commonly available food types": get_most_common_food_types,
    "Number of claims per food item": get_food_claims_per_item,
    "Provider with highest successful claims": get_top_successful_provider,
    "Percentage of claims completed/pending/canceled": get_claim_status_percentage,
    "Average quantity claimed per receiver": get_avg_claimed_quantity_per_receiver,
    "Most claimed meal type": get_most_claimed_meal_type,
    "Total quantity donated by each provider": get_total_donated_by_provider,
}

chart_types = ["Table", "Bar Chart", "Pie Chart", "Line Chart"]

# ---- Visualization Section ----
st.markdown("<h1 style='text-align: center; color: white;'>📊 Data Visualization</h1>", unsafe_allow_html=True)

selected_query = st.selectbox("Select a query to visualize:", list(query_mapping.keys()))
selected_chart = st.selectbox("Select a chart type:", chart_types)

# ---- Special Parameter Handling ----
params = {}
if selected_query == "Provider contacts in a specific city":
    params["city"] = st.text_input("Enter city name:")

if st.button("Show Visualization"):
    conn = get_connection()
    cursor = conn.cursor()

    # Fetch data
    if params:
        cursor.execute(query_mapping[selected_query](**params))
    else:
        cursor.execute(query_mapping[selected_query]())

    data = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    df = pd.DataFrame(data, columns=columns)

    cursor.close()
    conn.close()

    if df.empty:
        st.warning("⚠️ No data found for this query.")
    else:
        if selected_chart == "Table":
            st.dataframe(df)
        elif selected_chart == "Bar Chart":
            chart = alt.Chart(df).mark_bar().encode(
                x=alt.X(df.columns[0], sort=None),
                y=df.columns[1]
            )
            st.altair_chart(chart, use_container_width=True)
        elif selected_chart == "Pie Chart":
            fig, ax = plt.subplots()
            ax.pie(df.iloc[:, 1], labels=df.iloc[:, 0], autopct="%1.1f%%")
            ax.axis("equal")
            st.pyplot(fig)
        elif selected_chart == "Line Chart":
            chart = alt.Chart(df).mark_line(point=True).encode(
                x=alt.X(df.columns[0], sort=None),
                y=df.columns[1]
            )
            st.altair_chart(chart, use_container_width=True)

st.markdown("---")
