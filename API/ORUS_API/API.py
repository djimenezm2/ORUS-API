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

def start(app: Flask, api: Api, swagger: Swagger, data_dir: str) -> None:
    """
    This function is the entry point for the API.

    Args:
        - app (flask.Flask): The Flask app object.
        - api (flask_restful.Api): The API object.
        - swagger (flasgger.Swagger): The Swagger object.
        - data_dir (str): The path to the data directory.

    Returns:
        # TODO: Define the return type.

    Raises:
        # TODO: Define the exceptions that are raised by this function.
    """

    logs_handler = logger.init(data_dir)
    logs_handler.info("\n" + "#" * 100 + "\n" )
    logs_handler.info("Starting the API...")

    db_connection = connect_database(logs_handler, data_dir)
    pass


def connect_database(logs_handler: logging.Logger, data_dir: str) -> mysql.connector.MySQLConnection:
    """
    This function connects to the database.
    It sets the credentials in the environment variables and then connects to the database.
    If there is an error in connecting to the database, it logs the error and exits the program.

    Args:
        - logs_handler (logging.Logger): The logger object.
        - data_dir (str): The path to the data directory.

    Returns:
        - db_connection (mysql.connector.MySQLConnection): The connection object.

    Raises:
        - mysql.connector.Error: If there is an error in connecting to the database.
    """

    logs_handler.info("Getting the credentials for de API DB user...")
    credentials_aquired = credentials_manager.set_credentials(data_dir) # Set the credentials in the environment variables.

    if not credentials_aquired: # If the credentials are not set successfully.
        logs_handler.error("An error occurred while setting the credentials.")
        exit(1)

    else: # If the credentials are set successfully.
        logs_handler.info("Credentials set successfully!")

    # Get the credentials from the environment variables.
    user = str(os.environ["API_DB_USER"])
    password = str(os.environ["API_DB_PASSWORD"])

    logs_handler.info("Attempting DB connection...")
    db_connection = db_connections.init(user, password) # Initialize the connection to the database.

    if type(db_connection) is mysql.connector.Error: # If there is an error in connecting to the database.
        logs_handler.error(f"An error occurred while connecting to the database: {db_connection}")
        exit(1)

    else:
        logs_handler.info("DB connection successful!")

        return db_connection