import os
import sys

# Get the current directory of the file.
parent_dir = os.path.dirname(__file__)

# Change the current working path to the parent directory of the file.
sys.path.insert(0, os.path.abspath(parent_dir))

data_dir = os.path.join(parent_dir, "data")

