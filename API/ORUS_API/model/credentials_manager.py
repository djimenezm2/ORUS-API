import os

def set_credentials_db() -> bool:
    """
    This function sets the credentials for the API DataBase user in the OS environment variables.

    Args:
        None

    Returns:
        - Bool: True if the credentials are set successfully, False otherwise.

    Raises:
        - FileNotFoundError: If the credentials file is not found.
    """

    data_dir = os.environ.get("data_dir") # Get the data directory from the environment variables.
    credentials = open_credentials_file(data_dir) # Open the credentials file.

    if type(credentials) is FileNotFoundError: # If the file is not found.
        return credentials

    else: # If the file is found.
        user = credentials.split("\n")[0]; password = credentials.split("\n")[1] # Get the user and password from the file.

        # Set the credentials in the environment variables.
        os.environ["API_DB_USER"] = user
        os.environ["API_DB_PASSWORD"] = password

        return True

def set_credentials_mqtt() -> bool:
    """
    This function sets the credentials for the API Broker MQTT in the OS environment variables.
    Is the same shit as the DB user, but for the mqtt.

    Args:
        None

    Returns:
        - Bool: True if the credentials are set successfully, False otherwise.

    Raises:
        - ConnectionRefusedError: If there is an error in connecting to the broker server.
        - OSError: If there is an error in connecting related to OS system.
        - Exception: If there is an unexpected error.
    """
    data_dir = os.environ.get("data_dir") # Get the data directory from the environment variables.
    credentials = open_credentials_file(data_dir) # Open the credentials file.

    if type(credentials) is FileNotFoundError: # If the file is not found.
        return credentials

    else: # If the file is found.
        user = credentials.split("\n")[2]; password = credentials.split("\n")[3]
        url = credentials.split("\n")[4]; topic = credentials.split("\n")[5]

        # Set the credentials in the environment variables.
        os.environ["API_MQTT_USER"] = user
        os.environ["API_MQTT_PASSWORD"] = password
        os.environ["API_MQTT_URL"] = url
        os.environ["API_MQTT_TOPIC"] = topic

        return True


def open_credentials_file(data_dir: str) -> str:
    """
    This function opens the credentials file and returns the contents.

    Args:
        - data_dir (str): The path to the data directory.

    Returns:
        - str: The contents of the credentials file.

    Raises:
        - FileNotFoundError: If the credentials file is not found.
    """

    credentials_file_path = f"{data_dir}/credentials.txt" # The path to the credentials file.

    try: # Try to open the file.
        with open(credentials_file_path, "r") as file:
            return file.read()

    except FileNotFoundError: # If the file is not found.
        return FileNotFoundError(f"The credentials file was not found at {credentials_file_path}")

