# Importing all the required modules
from controller import broker_connections, db_connections
from model import credentials_manager, logger
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
    logs_handler = logger.init()
    logs_handler.info("\n\n" + "#" * 100 + "\n" )
    logs_handler.info("Starting the API...")

    # Connect to the database.
    db_connection = connect_database(logs_handler)

    # Connect to the broker mqtt.
    broker_connection = connect_broker(logs_handler)
    pass


def connect_database(logs_handler: logging.Logger) -> mysql.connector.MySQLConnection:
    """
    This function connects to the database.
    It sets the credentials in the environment variables and then connects to the database.
    If there is an error in connecting to the database, it logs the error and exits the program.

    Args:
        - logs_handler (logging.Logger): The logger object.

    Returns:
        - db_connection (mysql.connector.MySQLConnection): The connection object.

    Raises:
        - mysql.connector.Error: If there is an error in connecting to the database.
    """

    logs_handler.info("Getting the credentials for de API DB user...")
    credentials_aquired = credentials_manager.set_credentials_db() # Set the credentials in the environment variables.

    if credentials_aquired is not True: # If the credentials are not set successfully.
        logs_handler.error("An error occurred while setting the credentials. See the error below:")
        logs_handler.error(f"Error: {credentials_aquired}")
        exit(1)

    else: # If the credentials are set successfully.
        logs_handler.info("Credentials set successfully!")

    # Get the credentials from the environment variables.
    user = str(os.environ["API_DB_USER"]); password = str(os.environ["API_DB_PASSWORD"])

    logs_handler.info("Attempting DB connection...")
    db_connection = db_connections.init(user, password) # Initialize the connection to the database.


    if type(db_connection) is not mysql.connector.connection_cext.CMySQLConnection: # If there is an error in connecting to the database.
        logs_handler.error(f"An error occurred while connecting to the database. See the error below:")
        logs_handler.error(f"Error: {db_connection}")
        exit(1)

    else:
        logs_handler.info("DB connection successful!")

        return db_connection

def connect_broker(logs_handler: logging.Logger):
    """
    This function connects to the broker mqtt.
    It sets the credentials in the environment variables and then connects to the broker mqtt.
    If there is an error in connecting to the broker, it logs the error and exits the program.

    Args:
        - logs_handler (logging.Logger): The logger object.

    Returns:
        - broker_connection (paho.mqtt.client.Client): The client object.

    Raises:
        - ConnectionRefusedError: If there is an error in connecting to the broker server.
        - OSError: If there is an error in connecting related to OS system.
        - Exception: If there is an unexpected error.
    """

    logs_handler.info("Getting the credentials for de API Broker MQTT...")
    credentials_aquired = credentials_manager.set_credentials_mqtt() # Set the credentials in the environment variables.

    if credentials_aquired is not True: # If the credentials are not set successfully.
        logs_handler.error("An error occurred while setting the mqtt credentials. See the error below:")
        logs_handler.error(f"Error: {credentials_aquired}")
        exit(1)

    else: # If the credentials are set successfully.
        logs_handler.info("Credentials for MQTT set successfully!")

    # Get the credentials from the environment variables.
    user = str(os.environ["API_MQTT_USER"]); password = str(os.environ["API_MQTT_PASSWORD"])
    url = str(os.environ["API_MQTT_URL"]); topic = str(os.environ["API_MQTT_TOPIC"])

    logs_handler.info("Attempting MQTT connection...")
    broker_connection = broker_connections.init(url, user, password, topic) # Initialize the connection to the broker mqtt.

    if type(broker_connection) is not mqtt.Client: # If there is an error in connecting to the broker.
        logs_handler.error(f"An error occurred while connecting to the MQTT broker. See the error below:")
        logs_handler.error(f"Error: {broker_connection}")

    else:
        logs_handler.info("Broker MQTT connection successful!")
        return broker_connection
