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
    # Get single book title from URL like: /fetch?title=Hobbit
    book_title = request.args.get('title', 'My_inventions').strip()
    
    if not book_title:
        return jsonify({"error": "Please provide 'title' parameter"}), 400
    
    # Step 1: Find the work ID for the given book title
    search_url = f"https://openlibrary.org/search.json?q={requests.utils.quote(book_title)}"
    search_response = requests.get(search_url)
    
    if search_response.status_code != 200:
        return jsonify({"error": "Failed to search for book"}), 500
    
    search_data = search_response.json()
    if not search_data.get("docs"):
        return jsonify({"error": "Book not found"}), 404
    
    # Get the first matching work
    work_key = search_data["docs"][0].get("key")
    if not work_key:
        return jsonify({"error": "No work key found for this book"}), 404
    
    # Step 2: Get the "similar books" from the work page
    work_url = f"https://openlibrary.org{work_key}.json"
    work_response = requests.get(work_url)
    
    if work_response.status_code != 200:
        return jsonify({"error": "Failed to fetch work details"}), 500
    
    work_data = work_response.json()
    
    # Try to get recommendations from different possible fields
    recommendations = []
    cover_ids = []
    # Option 3: Fallback to subject-based recommendations if no direct relations found
    if not recommendations and work_data.get("subjects"):
        for subject in work_data["subjects"][:3]:  # Take top 3 subjects
            subject_url = f"https://openlibrary.org/subjects/{subject.lower().replace(' ', '_')}.json?limit=5"
            subject_response = requests.get(subject_url)
            if subject_response.status_code == 200:
                subject_data = subject_response.json()
                recommendations.extend([(work["title"], work["cover_id"]) for work in subject_data.get("works", [])])

    unique_data = tuple(list(item) for item in {tuple(item) for item in recommendations})
    return render_template('questions.html', books=unique_data)
