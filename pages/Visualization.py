import streamlit as st
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt
import seaborn as sns
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
        password="root1234",
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

chart_options={
     "Food providers and receivers in each city": ["Table","Heatmap"],
    "Provider type contributing the most food": ["Table","Pie chart"],
    "Provider contacts in a specific city": ["Table"],
    "Receivers with the most food claims": ["Table"],
    "Total quantity of food available": ["Table"],
    "City with the highest number of food listings": ["Table","Seaborn Bar chart","Line chart","Heatmap"],
    "Most commonly available food types":  ["Table","Seaborn Bar chart","Line chart","Heatmap","Pie chart"] ,
    "Number of claims per food item": ["Table"],
    "Provider with highest successful claims": ["Table"],
    "Percentage of claims completed/pending/canceled": ["Table","Pie chart"],
    "Average quantity claimed per receiver": ["Table"],
    "Most claimed meal type":["Table","Seaborn Bar chart","Line chart" ,"Bar chart","Pie chart"],
    "Total quantity donated by each provider": ["Table"],

}

chart_types = ["Table", "Bar Chart", "Pie Chart", "Line Chart", "Seaborn Bar Chart", "Seaborn Heatmap"]

# ---- Visualization Section ----
st.markdown("<h1 style='text-align: center; color: black;'> Data Visualization</h1>", unsafe_allow_html=True)

selected_query = st.selectbox("Select a query to visualize:", list(query_mapping.keys()))

# Get allowed charts for this query
allowed_charts = chart_options.get(selected_query, ["Table"])  # default to Table
selected_chart = st.selectbox("Select a chart type:", allowed_charts)

# ---- Special Parameter Handling ----
params = {} 
if selected_query == "Provider contacts in a specific city":
    city_name = st.text_input("Enter city name:")

if st.button("Show Visualization"):
    conn = get_connection()
    cursor = conn.cursor()

    query = query_mapping[selected_query]()  # get query string

    # Execute with or without parameters
    if selected_query == "Provider contacts in a specific city" and city_name:
        cursor.execute(query, (city_name,))
    else:
        cursor.execute(query)

    data = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    df = pd.DataFrame(data, columns=columns)

    cursor.close()
    conn.close()

    if df.empty:
        st.warning("⚠️ No data found for this query.")
    else:
        # Automatically select a default chart for some queries

        if selected_chart == "Table":
            st.dataframe(df)
        elif selected_chart == "Bar chart":
            chart = alt.Chart(df).mark_bar().encode(
                x=alt.X(df.columns[0], sort=None),
                y=df.columns[1]
            )
            st.altair_chart(chart, use_container_width=True)
        elif selected_chart == "Line chart":
            chart = alt.Chart(df).mark_line(point=True).encode(
                x=alt.X(df.columns[0], sort=None),
                y=df.columns[1]
            )
            st.altair_chart(chart, use_container_width=True)
        elif selected_chart == "Pie chart":
            fig, ax = plt.subplots()
            ax.pie(df.iloc[:, 1], labels=df.iloc[:, 0], autopct="%1.1f%%")
            ax.axis("equal")
            st.pyplot(fig)
        elif selected_chart == "Seaborn Bar chart":
            fig, ax = plt.subplots()
            sns.barplot(x=df.columns[0], y=df.columns[1], data=df, ax=ax)
            ax.set_xlabel(df.columns[0])
            ax.set_ylabel(df.columns[1])
            st.pyplot(fig)
        elif selected_chart == "Heatmap":
            fig, ax = plt.subplots()
            sns.heatmap(df.set_index(df.columns[0]), annot=True, fmt="g", cmap="YlGnBu", ax=ax)
            st.pyplot(fig)
if st.button("⬅️ Back to Home"):
    st.switch_page("app.py")  # or the page you use for providers.py
    st.rerun()
st.markdown("---")
