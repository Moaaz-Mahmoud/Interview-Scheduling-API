import os
from app import app

# Get the path to the database file from the app configuration
db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', 'instance/')

if os.path.exists(db_path):
    os.remove(db_path)
    print("Database file deleted.")
else:
    print("Database file not found.")
