# Importing the required libraries
import mysql.connector


def init(user: str, password: str) -> mysql.connector.MySQLConnection:
    """
    This function initializes the connection to the database.

    Args:
        - user (str): The username for the database.
        - password (str): The password for the database.

    Returns:
        - db_connection (mysql.connector.MySQLConnection): The connection object.

    Raises:
        - mysql.connector.Error: If there is an error in connecting to the database.
    """

    try: # Try to connect to the database.
        db_connection = mysql.connector.connect( # Connect to the database.
            host = "127.0.0.1",
            user = user,
            password = password
        )

        if db_connection.is_connected():
            return db_connection

        else:
            raise mysql.connector.Error("Error in connecting to the database.")

    except mysql.connector.Error as error: # If there is an error in connecting to the database.
        return error