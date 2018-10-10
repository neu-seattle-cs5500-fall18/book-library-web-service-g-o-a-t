
from flask import Flask
from flask_restplus import Api, Resource

app = Flask(__name__)
api = Api(app)


@app.route('/Book')
class Book:
    def __init__(self, ID, title, author, genre, year_released, checked_out):
        Book.title = title
        Book.author = author
        Book.ID = ID
        Book.genre = genre
        Book.year_released = year_released
        Book.checked_out = checked_out
        Book.deleted = False

