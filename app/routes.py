from flask import render_template  # <- This imports HTML templates
from app import app  # Import the Flask app
from flask import request, jsonify  # Add this import
import requests
from bs4 import BeautifulSoup
import urllib.parse
topics = []
@app.route("/")
def home():
    return render_template('questions.html', title='Home Page') 

@app.route("/about")
def about():
    return render_template("about.html", title="About Us")

@app.route('/process', methods=['POST'])
def process():
    # Get JSON data from the request
    data = request.get_json()  # Parse incoming JSON
    user_input = data.get('user_input')  # Extract the value
    topics.append(user_input)
    print(topics)

   

    # Return a JSON response
    return jsonify({
        'status': 'success',
        'message': 'Data received!',
        'input': user_input
    })

@app.route('/fetch', methods=['GET'])
def fetch():
    # Get comma-separated book titles from URL like:
    # /fetch?book_titles=Hobbit,Dune,Pride+and+Prejudice
    book_titles_str = request.args.get('book_titles', 'Einführung in Python,Hacking for dummies,Discrete Mathematics,Transactions on Engineering Technologies')
    book_titles = [title.strip() for title in book_titles_str.split(',') if title.strip()]
    
    if not book_titles:
        return jsonify({"error": "Please provide 'book_titles' parameter (comma-separated)"}), 400
    
    subjects = set()
    # Step 1: Get genres/subjects of all input books
    for title in book_titles:
        search_url = f"https://openlibrary.org/search.json?q={requests.utils.quote(title)}"
        book_data = requests.get(search_url).json()
        if book_data.get("docs"):
            book_subjects = book_data["docs"][0].get("subject", ['Computer science','Mathematics'])
            subjects.update(book_subjects[:3])  # Take top 3 subjects per book
    
    # Step 2: Find books that share the most subjects
    recommendations = []
    for subject in subjects:
        rec_url = f"https://openlibrary.org/subjects/{subject.lower()}.json?limit=5"
        rec_data = requests.get(rec_url).json()
        recommendations.extend([work["title"] for work in rec_data.get("works", [])])
    
    # Remove duplicates and input books

    unique_recs = list(set(recommendations) - set(book_titles))[:10]  # Top 10 unique recs
    return jsonify({"recommendations": unique_recs})
