import pandas as pd
import mysql.connector
from datetime import datetime

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root1234",  # change to your MySQL password
        database="food_donation"
    )

## How many food providers and receivers are there in each city?
def food_providers_receivers_by_city():
    conn = get_connection()
    query = """
    SELECT city, 
           COUNT(DISTINCT provider_id) AS providers,
           COUNT(DISTINCT receiver_id) AS receivers
    FROM food_listings
    GROUP BY location;
    """
    return pd.read_sql(query, conn)