# Booket

Booket is a web application that recommends books based on your favorite books and their subjects.  
It uses the OpenLibrary API along with a custom recommendation algorithm to suggest books you might love.  
Built with **Flask**.

## Features

- Input your favorite books.
- Get personalized book recommendations based on the subjects of your favorites.
- Powered by the OpenLibrary API.
- Custom-built recommendation algorithm.

## Technologies Used

- Python
- Flask
- OpenLibrary API
- HTML/CSS (for frontend)

## How It Works

1. You enter your favorite books.
2. Booket fetches their subjects using the OpenLibrary API.
3. Booket's custom algorithm analyzes the subjects and suggests similar books.
4. You receive personalized book recommendations!

## Installation

1. Clone the repository:

```bash
git clone https://github.com/mohamed-chafik/booklet.git
```

2. Navigate into the project directory:

```bash
cd booklet
```

3. Install the dependencies:

```bash
pip install -r requirements.txt
```

4. Run the application:

```bash
python run.py
```

5. Open your browser and go to:

```
http://localhost:5000
```



## Future Improvements

- Add user accounts and save favorites.
- Improve the recommendation algorithm.
- Add more filtering options (e.g., genre, author, publication year).
- Mobile-friendly design.



Feel free to contribute and help make Booket even better!
