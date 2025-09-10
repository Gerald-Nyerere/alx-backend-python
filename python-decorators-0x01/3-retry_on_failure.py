import time
import sqlite3 
import functools

#### with_db_connection decorator
def with_db_connection(func):
    """Decorator that opens a DB connection, passes it to the function, and closes it after"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        try:
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
        return result
    return wrapper


#### retry_on_failure decorator
def retry_on_failure(retries=3, delay=2):
    """Decorator that retries a function call if it raises an exception"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    print(f"[Retry {attempt}/{retries}] Error: {e}. Retrying in {delay}s...")
                    time.sleep(delay)
            # Raise last exception if all retries fail
            raise last_exception
        return wrapper
    return decorator



@with_db_connection
@retry_on_failure(retries=3, delay=1)

def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

#### attempt to fetch users with automatic retry on failure

users = fetch_users_with_retry()
print(users)