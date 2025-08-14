import pandas as pd
import mysql.connector

# ---- Database Connection ----
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root1234",  # change to your MySQL password
        database="food_donation"
    )

# ---- Helper: Fetch full table as DataFrame ----
def get_table(table_name):
    conn = get_connection()
    df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
    conn.close()
    return df

# =============================
# CRUD: Providers
# =============================
def add_provider(provider_id, name, type_, address, city, contact):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO providers (Provider_ID, Name, Type, Address, City, Contact)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (provider_id, name, type_, address, city, contact))
    conn.commit()
    conn.close()

def update_provider(provider_id, name, type_, address, city, contact):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE providers
        SET Name=%s, Type=%s, Address=%s, City=%s, Contact=%s
        WHERE Provider_ID=%s
    """, (name, type_, address, city, contact, provider_id))
    conn.commit()
    conn.close()

def delete_provider(provider_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM providers WHERE Provider_ID=%s", (provider_id,))
    conn.commit()
    conn.close()

# =============================
# CRUD: Receivers
# =============================
def add_receiver(receiver_id, name, type_, city, contact):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO receivers (Receiver_ID, Name, Type, City, Contact)
        VALUES (%s, %s, %s, %s, %s)
    """, (receiver_id, name, type_, city, contact))
    conn.commit()
    conn.close()

def update_receiver(receiver_id, name, type_, city, contact):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE receivers
        SET Name=%s, Type=%s, City=%s, Contact=%s
        WHERE Receiver_ID=%s
    """, (name, type_, city, contact, receiver_id))
    conn.commit()
    conn.close()

def delete_receiver(receiver_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM receivers WHERE Receiver_ID=%s", (receiver_id,))
    conn.commit()
    conn.close()

# =============================
# CRUD: Food Listings
# =============================
def add_food(food_id, food_name, quantity, expiry_date, provider_id, provider_type, location, food_type, meal_type):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO food_listings 
        (Food_ID, Food_Name, Quantity, Expiry_Date, Provider_ID, Provider_Type, Location, Food_Type, Meal_Type)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (food_id, food_name, quantity, expiry_date, provider_id, provider_type, location, food_type, meal_type))
    conn.commit()
    conn.close()

def update_food(food_id, food_name, quantity, expiry_date, provider_id, provider_type, location, food_type, meal_type):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE food_listings
        SET Food_Name=%s, Quantity=%s, Expiry_Date=%s, Provider_ID=%s, Provider_Type=%s, 
            Location=%s, Food_Type=%s, Meal_Type=%s
        WHERE Food_ID=%s
    """, (food_name, quantity, expiry_date, provider_id, provider_type, location, food_type, meal_type, food_id))
    conn.commit()
    conn.close()

def delete_food(food_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM food_listings WHERE Food_ID=%s", (food_id,))
    conn.commit()
    conn.close()

# =============================
# CRUD: Claims
# =============================
def add_claim(claim_id, food_id, receiver_id, status, timestamp):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO claims (Claim_ID, Food_ID, Receiver_ID, Status, Timestamp)
        VALUES (%s, %s, %s, %s, %s)
    """, (claim_id, food_id, receiver_id, status, timestamp))
    conn.commit()
    conn.close()

def update_claim(claim_id, food_id, receiver_id, status, timestamp):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE claims
        SET Food_ID=%s, Receiver_ID=%s, Status=%s, Timestamp=%s
        WHERE Claim_ID=%s
    """, (food_id, receiver_id, status, timestamp, claim_id))
    conn.commit()
    conn.close()

def delete_claim(claim_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM claims WHERE Claim_ID=%s", (claim_id,))
    conn.commit()
    conn.close()
