import mysql.connector
from mysql.connector import Error
import uuid
import csv

# Connect to MySQL server
def connect_db():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',       # Change if needed
            password='password'  # Change if needed
        )
        if connection.is_connected():
            print("Connected to MySQL server")
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

# Create Database ALX_prodev
def create_database(connection):
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
    print("Database ALX_prodev ensured.")


# Connect to ALX_prodev DB
def connect_to_prodev():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',        # Change if needed
            password='password', # Change if needed
            database='ALX_prodev'
        )
        if connection.is_connected():
            print("Connected to ALX_prodev database")
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

# Create user_data table
def create_table(connection):
    query = """
    CREATE TABLE IF NOT EXISTS user_data (
        user_id CHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age DECIMAL(3,0) NOT NULL,
        INDEX(user_id)
    )
    """
    cursor = connection.cursor()
    cursor.execute(query)
    print("Table user_data ensured.")


# Insert Data
def insert_data(connection, data):
    query = """
    INSERT INTO user_data (user_id, name, email, age)
    VALUES (%s, %s, %s, %s)
    """
    cursor = connection.cursor()

    for row in data:
        user_id = str(uuid.uuid4())
        name, email, age = row
        cursor.execute("SELECT email FROM user_data WHERE email = %s", (email,))
        if cursor.fetchone() is None:
            cursor.execute(query, (user_id, name, email, age))
            print(f"Inserted: {name}, {email}, {age}")
        else:
            print(f"Duplicate email skipped: {email}")
    connection.commit()


# Load Data from CSV
def load_csv_data(file_path):
    data = []
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  
        for row in reader:
            data.append(row)
    return data


# MAIN EXECUTION
if __name__ == "__main__":

    conn = connect_db()
    create_database(conn)
    conn.close()

    db_conn = connect_to_prodev()

    create_table(db_conn)

    sample_data = load_csv_data("user_data.csv")
    insert_data(db_conn, sample_data)

    db_conn.close()
