#!/usr/bin/python3
"""
Module: 1-batch_processing
Generates and processes user data in batches using generators.
"""

import mysql.connector


def stream_users_in_batches(batch_size):
    """
    Generator that fetches users in batches from the user_data table.
    Yields lists of user dictionaries, each of size batch_size (except possibly the last).
    """
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Volcanoe@&01",  # replace with your MySQL password
        database="ALX_prodev"
    )
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM user_data")

    batch = []
    for row in cursor:  # Loop 1
        batch.append(row)
        if len(batch) == batch_size:
            yield batch
            batch = []
    if batch:
        yield batch

    cursor.close()
    conn.close()


def batch_processing(batch_size):
    """
    Process users in batches, filtering only users over age 25.
    Prints each valid user dictionary.
    """
    import sys

    for batch in stream_users_in_batches(batch_size):  # Loop 2
        for user in batch:  # Loop 3
            if int(user["age"]) > 25:  # also convert Decimal to int
                try:
                    print({
                        "user_id": user["user_id"],
                        "name": user["name"],
                        "email": user["email"],
                        "age": int(user["age"])
                    })
                except OSError:
                    # Handle Windows + Git Bash head/pipe errors
                    sys.exit(0)

