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

    def sort_by_genre(self):
        




