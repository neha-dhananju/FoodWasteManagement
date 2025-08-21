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
def get_providers_and_receivers_per_city():
    query = """
        SELECT 
            city,
            COUNT(DISTINCT providers.Provider_ID) AS total_providers,
            COUNT(DISTINCT receivers.Receiver_ID) AS total_receivers
        FROM 
            (
                SELECT City FROM providers
                UNION
                SELECT City FROM receivers
            ) AS cities
        LEFT JOIN providers ON providers.City = cities.City
        LEFT JOIN receivers ON receivers.City = cities.City
        GROUP BY city
        ORDER BY city;
    """
    return query



## Which type of food provider (restaurant, grocery store, etc.) contributes the most food?

def get_top_contributing_provider_type():
    query = """
        SELECT 
            p.Type AS provider_type,
            SUM(f.Food_Quantity) AS total_food_contributed
        FROM 
            providers p
        JOIN 
            food_listings f 
            ON p.Provider_ID = f.Provider_ID
        GROUP BY 
            p.Type
        ORDER BY 
            total_food_contributed DESC
        LIMIT 1;
    """
    return query



## What is the contact information of food providers in a specific city?
def get_providers_contact_by_city():
    query = """
        SELECT 
            Name AS provider_name,
            Type AS provider_type,
            Contact AS contact_info
        FROM 
            providers
        WHERE 
            City = %s;
    """
    return query



## Which receivers have claimed the most food?
def get_top_receivers_by_claims():
    query = """
        SELECT 
            r.Receiver_ID,
            r.Name AS receiver_name,
            r.City,
            r.Contact,
            SUM(c.Claimed_Quantity) AS total_claimed
        FROM 
            claims c
        JOIN 
            receivers r ON c.Receiver_ID = r.Receiver_ID
        GROUP BY 
            r.Receiver_ID, r.Name, r.City, r.Contact
        ORDER BY 
            total_claimed DESC;
    """
    return query


