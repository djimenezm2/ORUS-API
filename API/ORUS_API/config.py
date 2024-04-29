import os
import sys

# Get the current directory of the project.
parent_dir = os.path.dirname(__file__)
sys.path.append(parent_dir) # Add the parent directory to the system path.

# Change the current working path to the parent directory of the project.
data_dir = os.path.join(parent_dir, "data")
os.environ["data_dir"] = data_dir # Set the data directory in the environment variables.
