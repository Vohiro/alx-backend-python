#!/usr/bin/python3
import mysql.connector
from mysql.connector import Error


def stream_users():
    """Generator that streams rows from user_data table one by one"""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",          # replace with your MySQL user
            password="Volcanoe@&01",  # replace with your MySQL password
            database="ALX_prodev"
        )

        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM user_data;")
            # one loop only, yielding rows
            for row in cursor:
                yield row

            cursor.close()
            connection.close()

    except Error as e:
        print(f"Error while streaming users: {e}")
        return
