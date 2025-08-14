import mysql.connector
import pandas as pd

# MySQL connection function
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root1234",  
        database="food_donation"
    )

# Read table
def get_table(table_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    data = cursor.fetchall()
    cols = [desc[0] for desc in cursor.description]
    conn.close()
    return pd.DataFrame(data, columns=cols)

# Add
def add_provider(provider_id, name, type_, address, city, contact):
    conn = get_connection()
    cursor = conn.cursor()
    sql = """
    INSERT INTO providers (Provider_ID, Name, Type, Address, City, Contact)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(sql, (provider_id, name, type_, address, city, contact))
    conn.commit()
    conn.close()

# Update
def update_provider(provider_id, city, contact):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "UPDATE providers SET City=%s, Contact=%s WHERE Provider_ID=%s"
    cursor.execute(sql, (city, contact, provider_id))
    conn.commit()
    conn.close()

# Delete
def delete_provider(provider_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM providers WHERE Provider_ID=%s", (provider_id,))
    conn.commit()
    conn.close()
