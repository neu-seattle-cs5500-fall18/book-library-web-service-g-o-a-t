from flask import Flask
from flask_restplus import Api, Resource

app = Flask(__name__)

api = Api(app)


@app.route('/Book')
class Library(object):
    def __init__(self, Library_Id, Books, Checkouts):
        Library.Library_Id = Library_Id
        Library.Books = Books
        Library.Checkouts = Checkouts
        Library.deleted = False

    def in_library(self, book):
        for x in self.Books:
            if x == book or x.title == book:
                return True
        return False

    def in_stock(self, book):
        for x in self.Books:
            if (x == book or x.title == book) and x.checked_out == False:
                return True
        return False

    def sort_by_genre(self, genre):
        result = []
        for x in self.Books:
            if x.genre == genre:
                result.append(x)
        return result

    def sort_by_title(self, title):
        result = []
        for x in self.Books:
            if x.title == title:
                result.append(x)
        return result

    def sort_by_author(self, author):
        result = []
        for x in self.Books:
            if x.author == author:
                result.append(x)
        return result

    def sort_by_year_released(self, year):
        result = []
        for x in self.Books:
            if x.year_released == year:
                result.append(x)
        return result

    def sort_released_after_year(self, year):
        result = []
        for x in self.Books:
            if x.year_released < year:
                result.append(x)
        return result

    def sort_released_before_year(self, year):
        result = []
        for x in self.Books:
            if x.year_released > year:
                result.append(x)
        return result
