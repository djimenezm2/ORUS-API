import os

def set_credentials(data_dir: str) -> bool:
    """
    This function sets the credentials for the API DataBase user in the OS environment variables.

    Args:
        - data_dir (str): The path to the data directory.

    Returns:
        - Bool: True if the credentials are set successfully, False otherwise.

    Raises:
        - FileNotFoundError: If the credentials file is not found.
    """

    credentials = open_credentials_file(data_dir) # Open the credentials file.

    if type(credentials) is FileNotFoundError: # If the file is not found.
        return False

    else: # If the file is found.
        user = credentials.split("\n")[0] # The first line is the username.
        password = credentials.split("\n")[1] # The second line is the password.

        # Set the credentials in the environment variables.
        os.environ["API_DB_USER"] = user
        os.environ["API_DB_PASSWORD"] = password

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

