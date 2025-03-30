from flask import Flask

app = Flask(__name__)  # Create the Flask app
app.config.from_object('config')  # Load settings from config.py

# Import routes at the end to avoid circular imports
from app import routes
