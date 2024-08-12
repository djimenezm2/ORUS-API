from datetime import datetime
import os
import re

def check(args: dict) -> None:
    """
    Checks that the arguments passed from the web clients are correct.

    Args:
        - args (dict): The arguments passed from the web clients.

    Returns:
        - args (dict): The arguments passed from the web clients after checking and sanitizing.

    Raises:
        - Exception: If there is an unexpected error.
    """

    try:
        API_DB_TABLES = os.environ.get("API_DB_TABLES") # Get the tables from the environment variables.
        db_tables = API_DB_TABLES.split() # Split the tables into a list.

        for key, value in args.items(): # Iterate over the arguments.
            if value is not None: # If the argument's value is not missing.
                sanitizeSQL(value) # Sanitize the argument to prevent SQL injection.

                if key == "table_id":
                    if value not in db_tables:
                        raise ValueError(f"Invalid table_id. Table ID: {value}")

                elif key == "start_date" or key == "end_date":
                    value = check_date(value) # Check the date format.

                    args[key] = value # Update the argument with the checked and converted value.

            else: # If the argument is missing.
                if key == "table_id": # If the argument is 'table_id' and it is missing.
                    raise ValueError("The argument 'table_id' is missing.")

        return args

    except Exception as error:
        raise error

def check_date(arg: str) -> str:
    """
    Checks the date format.

    Args:
        - arg (str): The date to check.

    Returns:
        - arg (str): The date after checking.

    Raises:
        - ValueError: If the date format is incorrect.
    """

    try:
        date = datetime.strptime(arg, "%Y-%m-%d %H:%M:%S") # Check the date format.

        if date >= datetime.now():
            arg = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return arg

    except Exception as error:
        raise ValueError(f"Incorrect date format ({arg}). The correct format is: 'YYYY-MM-DD HH:MM:SS'.")

def sanitizeSQL(arg: str) -> None:
    """
    Sanitizes the argument to prevent SQL injection.

    Args:
        - arg (str): The argument to sanitize.

    Returns:
        - None

    Raises:
        - ValueError: If there is an SQL injection detected in
    """

    try:
        # Prohibited patterns for SQL injection.
        prohibited_patterns = [";", "--", "/\\*", "\\*/", "'", "\"", "#"]

        for pattern in prohibited_patterns: # Iterate over the prohibited patterns.
            if re.search(pattern, arg): # If the pattern is found in the argument.
                raise ValueError(f"SQL injection detected in the argument: {arg}")

    except Exception as error:
        raise error
