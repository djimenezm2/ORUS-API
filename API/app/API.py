# Importing all the required modules
from connections import broker_connections, db_connections, web_connections
from utils import credentials_manager, logs_handler, data_checker, args_checker

# Importing the required libraries
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flasgger import Swagger
import logging
import mysql.connector
from datetime import datetime
import os

def start(app: Flask, api: Api, swagger: Swagger) -> None:
    """
    This function is the entry point for the API.

    Args:
        - app (flask.Flask): The Flask app object.
        - api (flask_restful.Api): The API object.
        - swagger (flasgger.Swagger): The Swagger object.

    Returns:
        - None

    Raises:
        - None
    """

    # Initialize the logger.
    logger = logs_handler.init()
    logger.info("\n\n" + "#" * 100 + "\n" )
    logger.info("Starting the API...")

    try:
        logger.info("Setting the credentials for the API...")
        credentials_manager.set_credentials() # Set the credentials in the environment variables.
        logger.info("Credentials set successfully!")

    except Exception as error:
        logger.error("An error occurred while setting the credentials. See the error below:")
        logger.error(f"Error: {error}")
        exit(1)

    # Connect to the database.
    logger.info("Attempting connection to the DataBase server...")
    db_connection, db_cursor = connect_database(logger)
    logger.info("DataBase connected successfully!")

    # Set the tables in the environment variables.
    set_db_tables(logger)

    # Connect to the broker mqtt.
    broker_connection = connect_broker(logger)

    # Start the web modules.
    start_web_services(logger, app, api, swagger)

    pass

def connect_database(logger: logging.Logger) -> mysql.connector.MySQLConnection:
    """
    This function connects to the database.
    It sets the credentials in the environment variables and then connects to the database.
    If there is an error in connecting to the database, it logs the error and exits the program.

    Args:
        - logger (logging.Logger): The logger object.

    Returns:
        - db_connection (mysql.connector.MySQLConnection): The connection object.
        - db_cursor (mysql.connector.cursor): The cursor object.
    """


    try:
        db_connection, db_cursor = db_connections.init() # Initialize the connection to the database.

        return db_connection, db_cursor

    except Exception as error:
        logger.error(f"An error occurred while connecting to the database. See the error below:")
        logger.error(f"Error: {error}")

        exit(1)

def connect_broker(logger: logging.Logger):
    """
    This function connects to the broker mqtt.
    It sets the credentials in the environment variables and then connects to the broker mqtt.
    If there is an error in connecting to the broker, it logs the error and exits the program.

    Args:
        - logger (logging.Logger): The logger object.

    Returns:
        - broker_connection (paho.mqtt.client.Client): The client object.

    """

    try:
        logger.info("Attempting connection to the MQTT Broker...")
        broker_connection = broker_connections.init(broker_on_message) # Initialize the connection to the broker mqtt.
        logger.info("MQTT Broker connected successfully!")

        return broker_connection

    except Exception as error:
        logger.error(f"An error occurred while connecting to the MQTT broker. See the error below:")
        logger.error(f"Error: {error}")

        exit(1)

def start_web_services(logger: logging.Logger, app: Flask, api: Api, swagger: Swagger) -> None:
    """
    This function starts the web services for the API.

    Args:
        - app (flask.Flask): The Flask app object.
        - api (flask_restful.Api): The API object.
        - swagger (flasgger.Swagger): The Swagger object.

    Returns:
        - None
    """

    @app.route("/OrusDashboard/API", methods = ["GET"])
    def execute_request():
        table_id = request.args.get("table_id") # Get the table id from the request.
        start_date = request.args.get("start_date") # Get the start date from the request.
        end_date = request.args.get("end_date") # Get the end date from the request.

        # Create a dictionary with the arguments.
        args = {"table_id": table_id, "start_date": start_date, "end_date": end_date}

        logger.info(f"Request received. Table ID: {table_id}, Start Date: {start_date}, End Date: {end_date}")

        try:
            logger.info("Checking the arguments...")
            args = args_checker.check(args) # Check the arguments passed from the web clients.
            logger.info("Arguments checked successfully!")

            table_id = args["table_id"]; start_date = args["start_date"]; end_date = args["end_date"] # Get the checked arguments.

            db_connection, db_cursor = connect_database(logger) # Connect to the database.

            logger.info("Executing the queries to get the data from the database...")
            query = f"SHOW columns FROM {table_id}"
            column_names = [column_name for column_name in db_connections.execute(db_cursor, query)]

            if start_date == None and end_date == None: # If the start and end dates are missing.
                query = f"SELECT * FROM {table_id}" # Query to get all the values from the table.

            elif end_date == None: # If the end date is missing.
                query = f"SELECT * FROM {table_id} WHERE DATE >= '{start_date}'" # Query to get the values from the start date.

            else: # If both the start and end dates are present.
                query = f"SELECT * FROM {table_id} WHERE DATE >= '{start_date}' AND DATE <= '{end_date}'" # Query to get the values between the start and end dates.

            data = [value for value in db_connections.execute(db_cursor, query)] # Execute the query to get the values from the table.
            logger.info("Queries executed successfully!")

            db_connections.close(db_connection, db_cursor) # Close the database connection.

            logger.info("Formatting the data to be returned to the client...")
            result = format_data(column_names, data) # Format the data to be returned to the client.
            logger.info("Data formatted successfully!")

            logger.info("Returning the result to the client...")

            return jsonify(result), 200

        except Exception as error:
            logger.error(f"An error occurred while processing the request. See the error below:")
            logger.error(f"Error: {error}")

            return jsonify(f"An error occurred while processing the request. Error: {error}"), 500

    try:
        logger.info("Starting the web services of the API...")
        web_connections.init(app, api, swagger)
        logger.info("Web services started successfully!")

    except Exception as error:
        logger.error(f"An error occurred while starting the web modules. See the error below:")
        logger.error(f"Error: {error}")

    pass

def set_db_tables(logger: logging.Logger) -> None:
    """
    This function sets the tables in the environment variables.

    Args:
        - logger (logging.Logger): The logger object.

    Returns:
        - None

    Raises:
        - None
    """

    try:
        logger.info("Setting the tables in the environment variables...")

        db_connection, db_cursor = connect_database(logger) # Connect to the database.
        db_tables = db_connections.execute(db_cursor, "SHOW TABLES") # Execute the query to get the tables in the database.

        db_tables_string = "" # Initialize the string to store the tables.

        for table in db_tables: # Iterate through the tables.
            db_tables_string += f"{table[0]} " # Add the table to the string.

        db_tables_string = db_tables_string.strip() # Strip the string to remove the trailing whitespace.
        os.environ["API_DB_TABLES"] = db_tables_string # Set the tables in the environment variables.

        db_connections.close(db_connection, db_cursor) # Close the database connection.

        logger.info("Tables set in the environment variables successfully!")

    except Exception as error:
        logger.error(f"An error occurred while setting the tables in the environment variables. See the error below:")
        logger.error(f"Error: {error}")

def broker_on_message(client, userdata, message):
    """
    This function is called by the mqtt client thread when a new message is received from the broker.

    Args:
        - client (paho.mqtt.client.Client): The client object.
        - userdata: The user data.
        - message (paho.mqtt.client.MQTTMessage): The message object.

    Returns:
        - None
    """

    logger = logs_handler.init() # Initialize the logger.

    try:

        logger.info("New message received from the MQTT broker, processing the message...")

        logger.info("Parsing the data received from the MQTT broker...")
        data = data_checker.parse_data(message.payload.decode("utf-8")) # Parse the data received from the broker.
        logger.info("Data parsed successfully!")

        db_connection, db_cursor = connect_database(logger) # Connect to the database.

        logger.info("Attempting to write the data to the database...")
        db_connections.write_data(db_cursor, data) # Write the data to the database.
        logger.info("Data written to the database successfully!")

        db_connections.close(db_connection, db_cursor) # Close the database connection.

    except Exception as error:
        logger.error(f"An error occurred while processing the message. See the error below:")
        logger.error(f"Error: {error}")

def format_data(column_names: list, data: list) -> list:
    """
    This function formats the data to be returned to the client.

    Args:
        - column_names (list): The column names of the table.
        - data (list): The data to be formatted.

    Returns:
        - result (list): The formatted data.

    Raises:
        - Exception: If there is an unexpected error.
    """

    try:
        result = [] # Initialize the result list.

        column_names = [column_name[0] for column_name in column_names] # Get the column names from the list

        for row in data: # Iterate over the rows in the data.
            # Creates a dictionary with the format {column_name: value}.
            result.append({column_names[i]: row[i] for i in range(len(row))}) # Add the row to the result list.

        return result

    except Exception as error:
        raise error
