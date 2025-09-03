import mysql.connector

# Database connection
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="yourpassword",
        database="ALX_prodev"
    )

# Generator to yield user ages one by one
def stream_user_ages():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT age FROM user_data")
    for (age,) in cursor:
        yield age
    cursor.close()
    conn.close()

# Function to calculate average age using generator without loading all data
def calculate_average_age():
    total = 0
    count = 0
    for age in stream_user_ages():
        total += float(age) 
        count += 1

    average_age = total / count if count > 0 else 0
    print(f"Average age of users: {average_age:.2f}")

if __name__ == "__main__":
    calculate_average_age()
