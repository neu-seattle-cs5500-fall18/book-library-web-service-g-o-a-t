from flask import request
from flask_restplus import Resource, Namespace, fields, reqparse
#import alchemy as book
api = Namespace('Books', description='Operations related to books')

books = []


class Book:
    def __init__(self, title, author, id, genre, year_released, checked_out, notes):
        self.title = title
        self.author = author
        self.id = id
        self.genre = genre
        self.year_released = year_released
        self.checked_out = checked_out
        self.notes = notes


book_model = api.model("Book", {
    'title': fields.String(description='Book title'),
    'author': fields.String(description='Book author'),
    'id': fields.Integer(description='Book ID'),
    'genre': fields.String(description='Book genre'),
    'year_released': fields.Integer(description='year released'),
    'checked_out': fields.String(description ='Is the book checked out'),
    'user_notes': fields.String(description = 'notes from user'),
})


parser = reqparse.RequestParser()
parser.add_argument('title', required=False)
parser.add_argument('author', required=False)
parser.add_argument('genre', required=False)
parser.add_argument('year_released', required=False)
parser.add_argument('checked_out', required=False)

@api.route('/')
@api.response(202, 'Accepted')
@api.response(404, 'Could not get a list of books')
class ListBookOperations(Resource):

    @api.expect(parser)
    def get(self):
        '''
        Returns list of books from given parameter.
        '''
        #TODO: add get method, using query from db

        return None

    @api.response(202, 'Accepted')
    @api.response(404, 'Could not create a new book')
    @api.expect(book_model, validate=True)
    def post(self):
        '''
        Creates a new book.
        '''
        data = request.json
        return None



@api.response(202, 'Accepted')
@api.response(404,'ID does not exist')
@api.route('/book/<int:id>')
#@api.doc(params={'id': 'An ID for a book'})
#@api.doc(params={'Title': 'The title for the book'})
#@api.doc(params={'Author': 'The author of the book'})
#@api.doc(params={'Genre': 'The genre of the book'})
#@api.doc(params={'YearReleased': 'The year the book was released'})
#@api.doc(params={'CheckedOut': 'Whether the book is checked out'})
class BookOperations(Resource):


    @api.response(404, 'Could not get specific book')
    def get(self, id):
        '''
        Returns a specific book.
        '''
        #TODO: add get method, using query from db
        return books

    @api.response(404, "could not update book")
    def put(self, id):
        '''

        Updates a book
        '''
        return None

    @api.response(404, "could not delete book")
    def delete(self, id):
        '''
        Deletes a book.
        '''
        #TODO: create delete_book method
        return None

