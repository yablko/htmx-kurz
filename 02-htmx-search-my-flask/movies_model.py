import json
from operator import attrgetter
import time
from threading import Thread
from random import random


# ========================================================
# Movie Model
# ========================================================
PAGE_SIZE = 25

class Movie:
	# mock movies database
	db = {}

	def __init__(self, id_=None, title=None, year=None, director=None, actors=None, plot=None):
		self.id = id_
		self.title = title
		self.year = year
		self.director = director
		self.actors = actors
		self.plot = plot
		self.errors = {}

	def __str__(self):
		return json.dumps(self.__dict__, ensure_ascii=False)

	@classmethod
	def count(cls):
		time.sleep(2)
		return len(cls.db)

	@classmethod
	def all(cls, page=1):
		page = int(page)
		start = (page - 1) * PAGE_SIZE
		end = start + PAGE_SIZE
		return list(cls.db.values())[start:end]

	@classmethod
	def search(cls, text):
		# time.sleep(2)

		result = []
		text = text.lower()

		for c in cls.db.values():
			match_title = c.title is not None and text in c.title.lower()
			match_director = c.director is not None and text in c.director.lower()
			match_actors = c.actors is not None and text in c.actors.lower()
			if match_title or match_director or match_actors:
				result.append(c)
				
		return result

	@classmethod
	def load_db(cls):
		with open('movies.json', 'r') as movies_file:
			movies = json.load(movies_file)
			cls.db.clear()
			for c in movies:
				cls.db[c['id']] = Movie(c['id'], c['title'], c['year'], c['director'], c['actors'], c['plot'])

	@classmethod
	def find(cls, id_):
		id_ = int(id_)
		c = cls.db.get(id_)
		if c is not None:
			c.errors = {}

		return c