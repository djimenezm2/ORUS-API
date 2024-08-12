# Importing the required libraries
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flasgger import Swagger
import waitress

def init(app: Flask, api: Api, swagger: Swagger) -> Flask:
    """
    This function initializes the web connections for the API.

    Args:
        - app (flask.Flask): The Flask app object.
        - api (flask_restful.Api): The API object.
        - swagger (flasgger.Swagger): The Swagger object.

    Returns:
        - app (flask.Flask): The Flask app object.

    Raises:
        - Exception: If there is an unexpected error.
    """

    try:
        waitress.serve(app, host = "127.0.0.1", port = 80) # Start the server.

        return app

    except Exception as error:
        raise error
