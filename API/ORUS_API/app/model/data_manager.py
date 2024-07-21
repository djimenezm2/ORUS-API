import json
from datetime import datetime
from model import logs_handler as logs_handler

def parse_data(data_json: str, db_tables: list) -> dict:
    """
    This function parses the data received from the MQTT broker.

    Args:
        - data_json (str): The data received from the MQTT broker.
        - db_tables (list): The tables for the database.

    Returns:
        - data (dict): The data parsed as a dictionary.
    """

    try:
        data_json = json.loads(data_json) # Parse the data to a dictionary.

        check_data(db_tables, data_json) # Confirm the keys for the database.

        data_json["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Add the timestamp to the data.
        data = dict(data_json) # Create a copy of the data.

        return data # Return the data.

    except Exception as error:
        raise error

def check_data(db_tables, data_json):
    """
    This function confirms that the keys and values are valid for the DB tables format.

    Args:
        - db_tables (list): The tables for the database.
        - data_json (dict): The data parsed as a dictionary.

    Returns:
        - None

    Raises:
        - KeyError: If the keys are not valid.
        - ValueError: If the values are not valid.
    """

    try:
        valid_keys = True; valid_values = True # Set the valid keys and valid values to True.

        for key, value in data_json.items(): # Iterate over the data.
            if valid_keys and valid_values: # If the keys and values are valid.
                if key != "CLIENT_ID" and (key,) in db_tables: # Check if the key is not the CLIENT_ID and is in the tables.
                    if isinstance(value, (int, float)) is True: # Check if the value is an integer or a float.
                        data_json[key] = round(float(value), 3) # Convert the value to a float and round it to 3 decimal places.

                    else: # If the value is an integer or a float.
                        valid_values = False # Set the valid_values to False and break the loop.
                        raise ValueError(f"Invalid values format. Message: {data_json}") # Raise a ValueError.

                elif key != "CLIENT_ID" and key not in db_tables: # If the key is not the CLIENT_ID and is not in the tables.
                    valid_keys = False
                    raise KeyError(f"Invalid keys format. Message: {data_json}") # Raise a KeyError.

    except Exception as error: # If there is an error in the data format.
        raise error