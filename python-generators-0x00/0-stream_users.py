import mysql.connector
from mysql.connector import Error


def stream_users():
    """
    A generator function that fetches rows one by one from the user_data table
    using a single loop and yield.
    """
    try:
        # Connect to ALX_prodev database
        connection = mysql.connector.connect(
            host='localhost',
            user='root',   # Change if necessary
            password='',   # Add password if any
            database='ALX_prodev'
        )

        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SELECT user_id, name, email, age FROM user_data;")

            # Fetch rows one by one and yield
            for row in cursor:
                yield row

            cursor.close()
            connection.close()

    except Error as e:
        print(f"Error fetching users: {e}")
