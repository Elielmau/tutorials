# Statements for enabling the development environment
DEBUG = True

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Define the database we are working with
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'chores.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
DATABASE_CONNECT_OPTIONS = {}

# Applications threads
THREADS_PER_PAGE = 2

# Protection against CSRF
CSRF_ENABLED = True
CSRF_SESSION_KEY = "b71df400c0dce8799bc90b60f1f35baaf35fb83bd74589c0"

# Secret key for signing cookies
SECRET_KEY = "dacae7cdb437d289350c12e3726bb9ab4a751bc669b197ec"

# For testing purposes
USERNAME = 'eliel'
USERS = ['evie', 'gael', 'admin']