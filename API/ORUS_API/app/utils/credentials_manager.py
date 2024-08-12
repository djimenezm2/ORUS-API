import os
import json

def set_credentials() -> bool:
    """
    This function sets the credentials for the API DataBase user and the API Broker MQTT in the OS environment variables.

    Args:
        - None

    Returns:
        - None

    Raises:
        - FileNotFoundError: If the credentials file is not found.
        - Exception: If there is an unexpected error.
    """

    try:
        data_dir = os.environ.get("data_dir") # Get the data directory from the environment variables.
        credentials = json.loads(open_credentials_file(data_dir)) # Open the credentials file and load the contents as a JSON object.

        database_credentials = credentials["database"] # Get the database credentials from the credentials.
        mqtt_credentials = credentials["mqtt"] # Get the mqtt credentials from the credentials.

        set_credentials_db(database_credentials) # Set the database credentials in the environment variables.
        set_credentials_mqtt(mqtt_credentials) # Set the mqtt credentials in the environment variables.

    except Exception as error:
        raise error

def set_credentials_db(database_credentials: dict) -> bool:
    """
    This function sets the credentials for the API DataBase in the OS environment variables.

    Args:
        - database_credentials (dict): The credentials for the database.

    Returns:
        - None

    Raises:
        - Exception: If there is an unexpected error.
    """

    try:
        # Set the credentials in the environment variables.
        os.environ["API_DB_HOST"] = database_credentials["host"]
        os.environ["API_DB_PORT"] = database_credentials["port"]
        os.environ["API_DB_USER"] = database_credentials["username"]
        os.environ["API_DB_PASSWORD"] = database_credentials["password"]
        os.environ["API_DB_TABLE"] = database_credentials["table"]

    except Exception as error: # If there is an error in setting the credentials.
        raise error

def set_credentials_mqtt(mqtt_credentials: dict) -> bool:
    """
    This function sets the credentials for the API MQTT Broker in the OS environment variables.

    Args:
        - mqtt_credentials (dict): The credentials for the MQTT Broker

    Returns:
        - None

    Raises:
        - Exception: If there is an unexpected error.
    """

    try:
        # Set the credentials in the environment variables.
        os.environ["API_MQTT_HOST"] = mqtt_credentials["host"]
        os.environ["API_MQTT_PORT"] = mqtt_credentials["port"]
        os.environ["API_MQTT_USER"] = mqtt_credentials["username"]
        os.environ["API_MQTT_PASSWORD"] = mqtt_credentials["password"]
        os.environ["API_MQTT_TOPIC"] = mqtt_credentials["topic"]

    except Exception as error: # If there is an error in setting the credentials.
        raise error

def open_credentials_file(data_dir: str) -> str:
    """
    This function opens the credentials file and returns the contents.

    Args:
        - data_dir (str): The path to the data directory.

    Returns:
        - str: The contents of the credentials file.

    Raises:
        - Exception: If there is an error while opening the file.
    """

    credentials_file_path = f"{data_dir}/credentials.json" # The path to the credentials file.

    try: # Try to open the file.
        with open(credentials_file_path, "r") as file:
            credentials = file.read() # Read the contents of the file.
            file.close() # Close the file.

            return credentials

    except Exception as error: # If there is an error in opening the file.
        raise error