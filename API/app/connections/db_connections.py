# Importing the required libraries
from utils import logs_handler

import mysql.connector
import os

def init() -> mysql.connector.MySQLConnection:
    """
    This function initializes the connection to the database.

    Args:
        - None

    Returns:
        - db_connection (mysql.connector.MySQLConnection): The connection object.
        - db_cursor (mysql.connector.cursor): The cursor object.

    Raises:
        - Exception: If there is an unexpected error.
    """

    # Get the credentials from the environment variables.
    host = str(os.environ["API_DB_HOST"]); port = int(os.environ["API_DB_PORT"])
    user = str(os.environ["API_DB_USER"]); password = str(os.environ["API_DB_PASSWORD"])
    table = str(os.environ["API_DB_TABLE"])

    try: # Try to connect to the database.
        db_connection = mysql.connector.connect( # Connect to the database.
            host = host,
            port = port,
            user = user,
            password = password,
        )

        if db_connection.is_connected():
            db_cursor = db_connection.cursor() # Create a cursor object.
            db_cursor.execute(f"use {table}") # Use the database table.

            return db_connection, db_cursor

        else:
            raise mysql.connector.Error("Error in connecting to the database.")

    except mysql.connector.Error as error: # If there is an error in connecting to the database.
        raise error

def close(db_connection: mysql.connector.MySQLConnection, db_cursor: mysql.connector.cursor):
    """
    This function closes the connection to the database.

    Args:
        - db_connection (mysql.connector.MySQLConnection): The connection object.
        - db_cursor (mysql.connector.cursor): The cursor object.

    Returns:
        - None

    Raises:
        - Exception: If there is an unexpected error.
    """

    try: # Try to close the connection to the database.
        db_cursor.close() # Close the cursor object.
        db_connection.close() # Close the connection object.

    except Exception as error: # If there is an error in closing the connection to the database.
        raise error

def write_data(db_cursor: mysql.connector.cursor, data: dict):
    """
    This function writes the data to the database.

    Args:
        - db_cursor (mysql.connector.cursor): The cursor object.
        - data (dict): The data to be written to the database.

    Returns:
        - None

    Raises:
        - Exception: If there is an error in writing the data to the database.
    """

    try: # Try to write the data to the database.
        CHIP_ID = data["CLIENT_ID"] # Get the CHIP_ID from the data.
        DATE = data["timestamp"] # Get the DATE from the data.

        db_cursor.execute("select CHIP_ID from iot_chips") # Select the CHIP_ID from the iot_chips table.
        chips = db_cursor.fetchall() # Fetch all the chips from the table.

        if (CHIP_ID,) not in chips: # If the CHIP_ID is not in the chips.
            db_cursor.execute("insert into iot_chips (CHIP_ID) values (%s)", (CHIP_ID,)) # Insert the CHIP_ID into the iot_chips table.
            db_cursor.execute("commit") # Commit the changes to the database.

        for key, value in data.items(): # Iterate over the data.
            if key != "CLIENT_ID" and key != "timestamp":
                db_cursor.execute(f"select DATA_ID from data_types where MEASURE_NAME = '{key}'") # Select the DATA_ID from the data_types table.
                DATA_ID = db_cursor.fetchone()[0] # Fetch the DATA_ID from the table.

                # Insert the data into the table.
                db_cursor.execute(f"insert into {key} (CHIP_ID, DATA_ID, VALUE, DATE) values (%s, %s, %s, %s)", (CHIP_ID, DATA_ID, value, DATE))
                db_cursor.execute('commit') # Commit the changes to the database.

    except Exception as error: # If there is an error in writing the data to the database.
        raise error

def execute(db_cursor: mysql.connector.cursor, query: str):
    """
    This function executes the query on the database.

    Args:
        - db_cursor (mysql.connector.cursor): The cursor object.
        - query (str): The query to be executed on the database.

    Returns:
        - db_cursor.fetchall(): The results of the query.

    Raises:
        - Exception: If there is an error in executing the query.
    """

    try: # Try to execute the query on the database.
        db_cursor.execute(query) # Execute the query on the database.

        return db_cursor.fetchall() # Return the results of the query.

    except Exception as error: # If there is an error in executing the query on the database.
        raise error