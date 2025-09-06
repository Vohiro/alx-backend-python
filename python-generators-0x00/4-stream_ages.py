#!/usr/bin/python3
"""
Module: 4-stream_ages
Compute memory-efficient average age using generators.
"""

import seed


def stream_user_ages():
    """
    Generator that yields ages of users one by one.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT age FROM user_data")
    for row in cursor:  # Loop 1
        # Convert Decimal to int if needed
        yield int(row["age"])

    cursor.close()
    connection.close()


def compute_average_age():
    """
    Computes and prints the average age of users without loading all data into memory.
    """
    total_age = 0
    count = 0

    for age in stream_user_ages():  # Loop 2
        total_age += age
        count += 1

    if count > 0:
        mean = total_age / count
        print(f"mean age of users: {mean:.2f}")
    else:
        print("No users found.")


if __name__ == "__main__":
    compute_average_age()
