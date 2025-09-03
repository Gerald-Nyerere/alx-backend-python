import mysql.connector
from mysql.connector import Error


def paginate_users(page_size, offset):
    """
    Fetch a single page of users from user_data table.
    :param page_size: Number of rows per page
    :param offset: Starting point for the query
    :return: List of rows for this page
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',    # Update if needed
            password='',    # Update if needed
            database='ALX_prodev'
        )

        if connection.is_connected():
            cursor = connection.cursor()
            query = "SELECT user_id, name, email, age FROM user_data LIMIT %s OFFSET %s;"
            cursor.execute(query, (page_size, offset))
            rows = cursor.fetchall()
            cursor.close()
            connection.close()
            return rows

    except Error as e:
        print(f"Error fetching page: {e}")
        return []


def lazy_paginate(page_size):
    """
    Generator function to lazily fetch paginated data.
    Fetches one page at a time using paginate_users().
    :param page_size: Number of rows per page
    :yield: A page (list of rows)
    """
    offset = 0
    while True:  # Only ONE loop
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size
