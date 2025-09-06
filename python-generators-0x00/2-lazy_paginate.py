#!/usr/bin/python3
"""
Module: 2-lazy_paginate
Simulates fetching paginated data lazily from the user_data table.
"""

import seed


def paginate_users(page_size, offset):
    """
    Fetches a page of users from the database.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    connection.close()
    return rows


def lazy_pagination(page_size):
    """
    Generator that lazily fetches pages of users.
    Yields one page at a time.
    """
    offset = 0
    while True:  # ✅ one loop
        page = paginate_users(page_size, offset)
        if not page:  # no more data
            break
        yield page
        offset += page_size
