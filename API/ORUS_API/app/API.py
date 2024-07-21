# Importing all the required modules
from controller import broker_connections, db_connections
from model import credentials_manager, logs_handler, data_manager
#from view import coms

# Importing the required libraries
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flasgger import Swagger
import os
import logging
import mysql.connector
import paho.mqtt.client as mqtt

def start(app: Flask, api: Api, swagger: Swagger) -> None:
    """
    This function is the entry point for the API.

    Args:
        - app (flask.Flask): The Flask app object.
        - api (flask_restful.Api): The API object.
        - swagger (flasgger.Swagger): The Swagger object.

    Returns:
        # TODO: Define the return type.

    Raises:
        # TODO: Define the exceptions that are raised by this function.
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
    global db_connection, db_cursor
    db_connection, db_cursor = connect_database(logger)

    # Connect to the broker mqtt.
    broker_connection = connect_broker(logger)

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
        logger.info("Attempting DB connection...")
        db_connection, db_cursor = db_connections.init() # Initialize the connection to the database.
        logger.info("DB connection successful!")

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
        logger.info("Attempting MQTT connection...")
        broker_connection = broker_connections.init(broker_on_message) # Initialize the connection to the broker mqtt.
        logger.info("Broker MQTT connection successful!")

        return broker_connection

    except Exception as error:
        logger.error(f"An error occurred while connecting to the MQTT broker. See the error below:")
        logger.error(f"Error: {error}")

        exit(1)

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
        global db_cursor # Get the global cursor object.
        logger.info("New message received from the MQTT broker, processing the message...")

        logger.info("Attempting to execute the query on the database...")
        db_tables = db_connections.execute(db_cursor, "Show tables;") # Execute the query to get the tables in the database.
        logger.info("Query executed on the database successfully!")


        logger.info("Parsing the data received from the MQTT broker...")
        data = data_manager.parse_data(message.payload.decode("utf-8"), db_tables) # Parse the data received from the broker.
        logger.info("Data parsed successfully!")

        logger.info("Attempting to write the data to the database...")
        db_connections.write_data(db_cursor, data) # Write the data to the database.
        logger.info("Data written to the database successfully!")

    except Exception as error:
        logger.error(f"An error occurred while processing the message. See the error below:")
        logger.error(f"Error: {error}")