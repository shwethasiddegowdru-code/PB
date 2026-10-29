
import mysql.connector
from mysql.connector import Error


def get_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="YOUR_MYSQL_PASSWORD",
            database="library_db"
        )

        if connection.is_connected():
            return connection

    except Error as e:
        print("Database connection failed:", e)
        raise
