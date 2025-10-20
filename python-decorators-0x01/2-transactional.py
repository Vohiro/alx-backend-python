import sqlite3
import functools

# ---------- Decorator 1: Handles connection opening/closing ----------
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
        return result
    return wrapper


# ---------- Decorator 2: Handles transaction management ----------
def transactional(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()  # Commit changes if successful
        except Exception as e:
            conn.rollback()  # Rollback changes on error
            print(f"[ERROR] Transaction rolled back due to: {e}")
            raise  # Re-raise the exception so it's not swallowed
        return result
    return wrapper


# ---------- Function that performs a DB update ----------
@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))
    print(f"[LOG] Updated user {user_id} email to {new_email}")


# ---------- Example usage ----------
update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
