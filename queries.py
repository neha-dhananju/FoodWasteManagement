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


## What is the total quantity of food available from all providers?

def get_total_available_food():
    query = """
        SELECT 
            SUM(Available_Quantity) AS total_available_food
        FROM 
            food_listings;
    """
    return query


## Which city has the highest number of food listings?
def get_city_with_highest_food_listings():
    query = """
        SELECT 
            Location AS city,
            COUNT(*) AS total_listings
        FROM 
            food_listings
        GROUP BY 
            Location
        ORDER BY 
            total_listings DESC
        LIMIT 1;
    """
    return query


## What are the most commonly available food types?
def get_most_common_food_types():
    query = """
        SELECT 
            Food_Type,
            COUNT(*) AS total_items
        FROM 
            food_listings
        GROUP BY 
            Food_Type
        ORDER BY 
            total_items DESC;
    """
    return query

## How many food claims have been made for each food item?
def get_food_claims_per_item():
    query = """
        SELECT 
            fl.Food_ID,
            fl.Food_Name,
            COUNT(c.Claim_ID) AS total_claims
        FROM 
            food_listings AS fl
        LEFT JOIN 
            claims AS c
        ON 
            fl.Food_ID = c.Food_ID
        GROUP BY 
            fl.Food_ID, fl.Food_Name
        ORDER BY 
            total_claims DESC;
    """
    return query


## Which provider has had the highest number of successful food claims?
def get_top_successful_provider():
    query = """
        SELECT 
            p.Provider_ID,
            p.Name AS Provider_Name,
            COUNT(c.Claim_ID) AS successful_claims
        FROM 
            claims AS c
        INNER JOIN 
            food_listings AS fl
            ON c.Food_ID = fl.Food_ID
        INNER JOIN 
            providers AS p
            ON fl.Provider_ID = p.Provider_ID
        WHERE 
            c.Status = 'Successful'
        GROUP BY 
            p.Provider_ID, p.Name
        ORDER BY 
            successful_claims DESC
        LIMIT 1;
    """
    return query


##  What percentage of food claims are completed vs. pending vs. canceled?
def get_claim_status_percentage():
    query = """
        SELECT 
            Status,
            COUNT(*) AS total_claims,
            ROUND((COUNT(*) * 100.0 / (SELECT COUNT(*) FROM claims)), 2) AS percentage
        FROM 
            claims
        GROUP BY 
            Status;
    """
    return query



##  What is the average quantity of food claimed per receiver?
def get_avg_claimed_quantity_per_receiver():
    query = """
        SELECT 
            r.Receiver_ID,
            r.Name AS Receiver_Name,
            ROUND(AVG(c.Claimed_Quantity), 2) AS avg_claimed_quantity
        FROM 
            claims c
        JOIN 
            receivers r ON c.Receiver_ID = r.Receiver_ID
        GROUP BY 
            r.Receiver_ID, r.Name
        ORDER BY 
            avg_claimed_quantity DESC;
    """
    return query

## Which meal type (breakfast, lunch, dinner, snacks) is claimed the most?
def get_most_claimed_meal_type():
    query = """
        SELECT 
            f.Meal_Type,
            SUM(c.Claimed_Quantity) AS total_claimed_quantity
        FROM 
            claims c
        JOIN 
            food_listings f ON c.Food_ID = f.Food_ID
        GROUP BY 
            f.Meal_Type
        ORDER BY 
            total_claimed_quantity DESC
        LIMIT 1;
    """
    return query


## What is the total quantity of food donated by each provider?
def get_total_donated_by_provider():
    query = """
        SELECT 
            p.Provider_ID,
            p.Name AS Provider_Name,
            SUM(f.Quantity) AS total_donated_quantity
        FROM 
            food_listings f
        JOIN 
            providers p ON f.Provider_ID = p.Provider_ID
        GROUP BY 
            p.Provider_ID, p.Name
        ORDER BY 
            total_donated_quantity DESC;
    """
    return query
