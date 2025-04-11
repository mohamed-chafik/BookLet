from flask import render_template  # <- This imports HTML templates
from app import app  # Import the Flask app

@app.route("/")
def home():
    return render_template('questions.html', title='Home Page') 

@app.route("/about")
def about():
    return render_template("about.html", title="About Us")
