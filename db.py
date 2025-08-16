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

def provider_id_exists(provider_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM providers WHERE provider_id = %s", (provider_id,))
    exists = cursor.fetchone() is not None
    cursor.close()
    conn.close()
    return exists

def provider_exists( name, type_, address, city, contact):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 1 FROM providers
        WHERE Name = %s
          AND Type = %s
          AND Address = %s
          AND City = %s
          AND Contact = %s
    """, ( name, type_, address, city, contact))
    exists = cursor.fetchone() is not None
    cursor.close()
    conn.close()
    return exists

def add_provider(provider_id, name, type_, address, city, contact):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO providers (Provider_ID, Name, Type, Address, City, Contact)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (provider_id, name, type_, address, city, contact))
   
    conn.commit()
    cursor.close()
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

def reciever_id_exists(receiver_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM receivers WHERE receiver_id = %s", (receiver_id,))
    exists = cursor.fetchone() is not None
    cursor.close()
    conn.close()
    return exists

def reciever_exists( name, type_, city, contact):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 1 FROM receivers
        WHERE Name = %s
          AND Type = %s
          AND Address = %s
          AND City = %s
          AND Contact = %s
    """, ( name, type_, city, contact))
    exists = cursor.fetchone() is not None
    cursor.close()
    conn.close()
    return exists

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

def food_id_exists(food_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM food_listings WHERE Food_ID = %s", (food_id,))
    exists = cursor.fetchone() is not None
    cursor.close()
    conn.close()
    return exists

def get_food_details(food_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM food_listings WHERE Food_ID = %s", (food_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result


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

def get_all_foods(provider_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT Food_ID, Food_Name FROM food_listings WHERE Provider_ID = %s", (provider_id,))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

def get_food_by_name(food_name):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM food_listings WHERE Food_Name = %s", (food_name,))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results


def get_food(provider_id, food_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT * FROM food_listings 
        WHERE Provider_ID = %s AND Food_ID = %s
    """, (provider_id, food_id))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result

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

def delete_food(provider_id, food_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM food_listings WHERE Provider_ID = %s AND Food_ID = %s",
        (provider_id, food_id)
    )
    conn.commit()
    cursor.close()
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
