import time
import sqlite3
import functools

# ------------------------------
# Decorator: Handles DB Connection
# ------------------------------
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("my_database.db")
        try:
            result = func(conn, *args, **kwargs)
            return result
        finally:
            conn.close()
    return wrapper


# ------------------------------
# Decorator: Retry on Failure
# ------------------------------
def retry_on_failure(retries=3, delay=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Attempt {attempt} failed with error: {e}")
                    if attempt == retries:
                        print("All retries failed.")
                        raise
                    else:
                        time.sleep(delay)
        return wrapper
    return decorator


# ------------------------------
# Example Usage
# ------------------------------
@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")  # may fail if table missing
    return cursor.fetchall()


# ------------------------------
# Test Run
# ------------------------------
try:
    users = fetch_users_with_retry()
    print(users)
except Exception as e:
    print("Final error:", e)
