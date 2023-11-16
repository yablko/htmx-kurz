from flask import (
	Flask, redirect, render_template, request, flash, jsonify, send_file
)

import time

from movies_model import Movie
Movie.load_db()

# ========================================================
# Flask App
# ========================================================

app = Flask(__name__)

# ========================================================
# Routes
# ========================================================


# INDEX
@app.route("/")
def index():
	search = request.args.get("q")

	if search:
		movies_set = Movie.search(search)
		if request.headers.get('HX-Trigger') == 'search':
			return render_template("index.html", movies=movies_set, s=search)
	else:
		page = request.args.get("page")
		page = page if page else 1
		movies_set = Movie.all(page)

	return render_template("index.html", movies=movies_set, s=search)


# SEARCH MOVIES
@app.route("/search")
def search():
	search = request.args.get("q")
	movies_set = []
	
	if search:
		time.sleep(0.25)
		movies_set = Movie.search(search)
	
	return render_template("search.html", movies=movies_set)


# FIND MOVIE
@app.route("/movie/<movie_id>")
def movie(movie_id = 0):
	if movie_id:
		movie_data = Movie.find(movie_id)
		return render_template("movie.html", movie=movie_data)


# ========================================================
# Run app
# ========================================================

if __name__ == "__main__":
	app.run(debug=True)