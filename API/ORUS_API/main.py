# Importing the config file
import config as cf
assert cf

# Importing the required libraries
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flasgger import Swagger

# Importing the required modules
import API

# Execution starts here:
if (__name__) == '__main__': # If the script is being run directly.
    app = Flask(__name__) # Create the Flask app object for the API.
    api = Api(app) # Create the API object for the app.
    swagger = Swagger(app) # Create the Swagger object for the app.

    API.start(app, api, swagger, cf.data_dir) # Start the API.