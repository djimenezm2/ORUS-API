# Importing the required libraries
import config as cf
assert cf

from flask import Flask
from flask_restful import Api, Resource
from flasgger import Swagger

# Importing the required modules
import API

# Execution starts here:
if (__name__) == '__main__': # If the script is being run directly.
    app = Flask(__name__) # Create the Flask app object for the API.
    api = Api(app) # Create the API object for the app.
    swagger = Swagger(app) # Create the Swagger object for the app.

    API.start(app, api, swagger) # Start the API.