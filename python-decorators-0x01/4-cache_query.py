import time
import sqlite3
import functools

# ------------------------------
# Global cache dictionary
# ------------------------------
query_cache = {}


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
# Decorator: Cache Query Results
# ------------------------------
def cache_query(func):
    @functools.wraps(func)
    def wrapper(conn, query, *args, **kwargs):
        if query in query_cache:
            print("Fetching result from cache...")
            return query_cache[query]

        print("Executing and caching new query...")
        result = func(conn, query, *args, **kwargs)
        query_cache[query] = result
        return result
    return wrapper


# ------------------------------
# Example usage
# ------------------------------
@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


# ------------------------------
# Test Run
# ------------------------------
users = fetch_users_with_cache(query="SELECT * FROM users")
print("First call:", users)

users_again = fetch_users_with_cache(query="SELECT * FROM users")
print("Second call (cached):", users_again)
