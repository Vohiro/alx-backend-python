#!/usr/bin/python3
import mysql.connector
from mysql.connector import Error
import csv
import uuid


def connect_db():
    """Connects to the MySQL database server"""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",          # change if your MySQL username is different
            password="Volcanoe@&01"   # change if you have a password set
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None


def create_database(connection):
    """Creates the database ALX_prodev if it does not exist"""
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
        cursor.close()
    except Error as e:
        print(f"Error creating database: {e}")


def connect_to_prodev():
    """Connects to the ALX_prodev database in MySQL"""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",          # change if needed
            password="Volcanoe@&01",  # change if needed
            database="ALX_prodev"
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error while connecting to ALX_prodev: {e}")
        return None


def create_table(connection):
    """Creates user_data table if it does not exist"""
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id CHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL NOT NULL,
                INDEX (user_id)
            );
        """)
        connection.commit()
        cursor.close()
        print("Table user_data created successfully")
    except Error as e:
        print(f"Error creating table: {e}")


def insert_data(connection, csv_file):
    """Inserts data into the database from CSV if it does not exist"""
    try:
        cursor = connection.cursor()
        with open(csv_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                user_id = str(uuid.uuid4())
                name = row["name"]
                email = row["email"]
                age = row["age"]

                # Check if record already exists
                cursor.execute("SELECT * FROM user_data WHERE email = %s", (email,))
                if cursor.fetchone():
                    continue  # skip duplicates

                cursor.execute("""
                    INSERT INTO user_data (user_id, name, email, age)
                    VALUES (%s, %s, %s, %s)
                """, (user_id, name, email, age))
        connection.commit()
        cursor.close()
    except Error as e:
        print(f"Error inserting data: {e}")
