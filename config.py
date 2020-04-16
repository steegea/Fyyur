import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

#   Connects to the database
#   Replace "*****" with your password
#   "fyyur" is the database name
SQLALCHEMY_DATABASE_URI = "postgres://postgres:root12345@localhost:5432/fyyur"
SQLALCHEMY_TRACK_MODIFICATIONS = False
