import pandas as pd
import mysql.connector
from mysql.connector import Error
from datetime import date,datetime

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
def get_provider(provider_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)  # returns results as dict
    cursor.execute("SELECT * FROM providers WHERE Provider_ID = %s", (provider_id,))
    provider = cursor.fetchone()
    cursor.close()
    conn.close()
    return provider

# =============================
# Custom Query: Receivers by Provider
# =============================
def get_receivers_by_provider(provider_id):
    """
    Fetch receivers who claimed food from a given provider,
    along with food and claim details.
    """
    conn = get_connection()
    query = """
        SELECT c.Claim_ID, r.Receiver_ID, r.Name AS Receiver_Name, r.Type, r.City AS Location, r.Contact,
               f.Food_ID,f.Food_Name, f.Expiry_Date, c.Status, c.Timestamp
        FROM claims c
        JOIN receivers r ON c.Receiver_ID = r.Receiver_ID
        JOIN food_listings f ON c.Food_ID = f.Food_ID
        WHERE f.Provider_ID = %s
    """
    df = pd.read_sql(query, conn, params=(provider_id,))
    conn.close()
    return df.to_dict(orient="records")


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
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO providers (Provider_ID, Name, Type, Address, City, Contact)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (provider_id, name, type_, address, city, contact))
   
        conn.commit()
    except Error as e:
        print("Error insering provider: ",e)
    finally:
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
    cursor.close()
    conn.close()


def delete_provider(provider_id):
    conn = get_connection()
    cursor = conn.cursor()
    # Delete food listings first to avoid foreign key issues
    cursor.execute("DELETE FROM food_listings WHERE Provider_ID = %s", (provider_id,))
    cursor.execute("DELETE FROM providers WHERE Provider_ID = %s", (provider_id,))
    conn.commit()
    cursor.close()
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


def get_food_by_provider(provider_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute( """
        SELECT Food_ID, Food_Name, Quantity, Expiry_Date, Provider_ID,
        Provider_Type, Location, Food_Type, Meal_Type
        FROM food_listings
        WHERE Provider_ID = %s
    """, (provider_id,))
    foods = cursor.fetchall()
    cursor.close()
    conn.close()
    return foods


def add_food(food_id, food_name, quantity, expiry_date, provider_id, provider_type, location, food_type, meal_type):
    """
    Adds a new food listing into the database.
    Handles duplicate IDs, foreign key issues, and commits data safely.
    """
    
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Convert expiry date to YYYY-MM-DD string
        if isinstance(expiry_date, date):
            expiry_date = expiry_date.strftime("%Y-%m-%d")

        cursor.execute("""
            INSERT INTO food_listings
            (Food_ID, Food_Name, Quantity, Expiry_Date, Provider_ID, Provider_Type,
             Location, Food_Type, Meal_Type)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,(food_id, food_name, quantity, expiry_date,
              provider_id, provider_type, location, food_type, meal_type))

        conn.commit()   

    except Error as e:
        # Handle duplicate Food_ID or foreign key constraint failures
        print("Error inserting food:", e)
    finally:
        cursor.close()
        conn.close()


def add_food_listing(food_id, food_name, quantity, expiry_date, location, food_type, meal_type, provider_id):
    conn = get_connection()
    cursor = conn.cursor()

    # Check if Food_ID already exists
    cursor.execute("SELECT 1 FROM food_listings WHERE Food_ID = %s", (food_id,))
    if cursor.fetchone():
        conn.close()
        return False  # Duplicate Food_ID

    # Insert new food record with Provider_ID
    query = """
        INSERT INTO food_listings 
        (Food_ID, Food_Name, Quantity, Expiry_Date, Location, Food_Type, Meal_Type, Provider_ID)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (food_id, food_name, quantity, expiry_date, location, food_type, meal_type, provider_id))
    conn.commit()
    conn.close()
    return True

    
       

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

def get_food_with_claims(provider_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT f.Food_ID, f.Food_Name, f.Quantity, f.Expiry_Date,
               f.Location, f.Food_Type, f.Meal_Type,
               COALESCE(r.Receiver_ID, '-') AS Receiver_ID,
               COALESCE(r.Name, '-') AS Receiver_Name,
               COALESCE(r.Type, '-') AS Receiver_Type,
               COALESCE(r.City, '-') AS Receiver_Location,
               COALESCE(r.Contact, '-') AS Receiver_Contact,
               COALESCE(c.Status, '-') AS Claim_Status,
               COALESCE(c.Timestamp, '-') AS Claim_Timestamp
        FROM food_listings f
        LEFT JOIN claims c ON f.Food_ID = c.Food_ID
        LEFT JOIN receivers r ON c.Receiver_ID = r.Receiver_ID
        WHERE f.Provider_ID = %s
    """
    cursor.execute(query, (provider_id,))
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data



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

def delete_food(food_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM food_listings WHERE Food_ID = %s", (food_id,))
    conn.commit()
    cursor.close()
    conn.close()


def update_food_listing(food_id, food_name, quantity, expiry_date, location, food_type, meal_type):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE food_listings
        SET Food_Name=%s, Quantity=%s, Expiry_Date=%s, Location=%s, Food_Type=%s, Meal_Type=%s
        WHERE Food_ID=%s
    """, (food_name, quantity, expiry_date, location, food_type, meal_type, food_id))
    conn.commit()
    cursor.close()
    conn.close()



# =============================
# CRUD: Claims
# =============================
def get_next_claim_id():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(Claim_ID) FROM claims")
    last_id = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return (last_id + 1) if last_id else 1  # start from 1 if table is empty


def add_claim(receiver_id, food_id, quantity):
    conn = get_connection()
    cursor = conn.cursor()
    # ✅ Step 1: Check if Receiver exists
    cursor.execute("SELECT COUNT(*) FROM receivers WHERE Receiver_ID = %s", (receiver_id,))
    if cursor.fetchone()[0] == 0:
        cursor.close()
        conn.close()
        return "Error: Receiver not found!"
    # ✅ Step 2: Check if Food exists
    cursor.execute("SELECT Quantity FROM food_listings WHERE Food_ID = %s", (food_id,))
    food = cursor.fetchone()
    if not food:
        cursor.close()
        conn.close()
        return "Error: Food item not found!"
    available_qty = food[0]
    # ✅ Step 3: Validate requested quantity
    if quantity > available_qty:
        cursor.close()
        conn.close()
        return f"Error: Only {available_qty} units available!"
    # ✅ Step 4: Generate next Claim ID
    claim_id = get_next_claim_id()
    # ✅ Step 5: Insert claim
    cursor.execute("""
        INSERT INTO claims (Claim_ID, Receiver_ID, Food_ID, Quantity, Status)
        VALUES (%s, %s, %s, %s, %s)
    """, (claim_id, receiver_id, food_id, quantity, "Pending"))
    # ✅ Step 6: Update available quantity in food_listings
    cursor.execute("""
        UPDATE food_listings 
        SET Quantity = Quantity - %s 
        WHERE Food_ID = %s
    """, (quantity, food_id))
    conn.commit()
    cursor.close()
    conn.close()
    return f"Claim {claim_id} added successfully! Pending approval."






def get_all_claims():
    conn = get_connection()
    query = """
        SELECT c.Claim_ID, c.Receiver_ID, r.Name as Receiver_Name,
               c.Food_ID, f.Food_Name, f.Quantity, c.Status
        FROM claims c
        JOIN receivers r ON c.Receiver_ID = r.Receiver_ID
        JOIN food_listings f ON c.Food_ID = f.Food_ID
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def get_claims_by_receiver(receiver_id):
    conn = get_connection()
    query = """
        SELECT c.Claim_ID, c.Receiver_ID, r.Name as Receiver_Name,
               c.Food_ID, f.Food_Name, f.Quantity, c.Status
        FROM claims c
        JOIN receivers r ON c.Receiver_ID = r.Receiver_ID
        JOIN food_listings f ON c.Food_ID = f.Food_ID
        WHERE c.Receiver_ID = %s
    """
    df = pd.read_sql(query, conn, params=(receiver_id,))
    conn.close()
    return df


def get_claim_by_id(claim_id, receiver_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT * FROM claims 
        WHERE Claim_ID=%s AND Receiver_ID=%s
    """, (claim_id, receiver_id))
    claim = cursor.fetchone()
    conn.close()
    return claim


def delete_claim(claim_id, receiver_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM claims 
        WHERE Claim_ID=%s AND Receiver_ID=%s
    """, (claim_id, receiver_id))
    conn.commit()
    conn.close()

def update_claim_status(claim_id, new_status, timestamp):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE claims 
        SET Status = %s, Timestamp = %s
        WHERE Claim_ID = %s
    """, (new_status, timestamp, claim_id))
    conn.commit()
    cursor.close()
    conn.close()

