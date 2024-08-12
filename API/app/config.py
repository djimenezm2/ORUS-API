import os
import sys

# Get the current directory of the app.
app_dir = os.path.dirname(__file__)

# Get the parent directory of the app.
parent_dir = os.path.dirname(app_dir)

sys.path.append(parent_dir) # Add the parent directory to the system path.

# Set the data directory.
data_dir = os.path.join(parent_dir, "data")
os.environ["data_dir"] = data_dir # Set the data directory in the environment variables.
