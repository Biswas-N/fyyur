import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database
# DATABASE URL
SQLALCHEMY_DATABASE_URI = 'postgresql://biswas@localhost:5432/fyyurdb' # Your database path here
SQLALCHEMY_TRACK_MODIFICATIONS = False