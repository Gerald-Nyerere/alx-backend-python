import mysql.connector
from mysql.connector import Error


def stream_users_in_batches(batch_size):
    """
    Generator that fetches rows in batches from the user_data table.
    :param batch_size: Number of rows to fetch per batch
    :yield: List of rows (batch)
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',  # Change if necessary
            password='',  # Add password if any
            database='ALX_prodev'
        )

        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SELECT user_id, name, email, age FROM user_data;")

            while True:  
                batch = cursor.fetchmany(batch_size)
                if not batch:
                    break
                yield batch  

            cursor.close()
            connection.close()

    except Error as e:
        print(f"Error fetching users in batches: {e}")


def batch_processing(batch_size):
    """
    Processes each batch of users and filters users over age 25.
    Uses generator for batch streaming.
    :param batch_size: Number of rows per batch
    :return: Users older than 25
    """
    for batch in stream_users_in_batches(batch_size):  
        for user in batch:  
            if int(user[3]) > 25:
                return user
