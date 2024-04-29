import os
import logging

def init() -> logging.Logger:
    """
    This function initializes the logger.

    Args:
        None

    Returns:
        - logger (logging.Logger): The logger object.

    Raises:
        - None
    """

    data_dir = os.environ["data_dir"] # Get the data directory from the environment variables.
    logs_dir = f"{data_dir}/logs" # The path to the logs directory.
    log_file_path = f"{data_dir}/logs/api.log"

    if not os.path.exists(logs_dir): # Create the logs directory if it does not exist.
        os.makedirs(logs_dir)

    logger = logging.getLogger() # Get the logger object.

    logging.basicConfig( # Configure the logger.
        filename = log_file_path,
        filemode = "a+",
        format = '%(asctime)s %(levelname)s %(levelno)s %(message)s',
        datefmt = "%m/%d/%Y %H:%M:%S",
        level = logging.INFO,
        encoding = "utf-8"
    )

    return logger