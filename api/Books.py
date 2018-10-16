from flask import request
from flask_restplus import Resource, Namespace, fields

api = Namespace('Books', description='Operations related to books')

books = []


class Book:
    def __init__(self, Title, Author, ID, Genre, Year_released, Checked_out):
        self.Title = Title
        self.Author = Author
        self.ID = ID
        self.Genre = Genre
        self.Year_released = Year_released
        self.Checked_out = Checked_out


book_model = api.model("Book", {
    'Title': fields.String(description='Book title'),
    'Author': fields.String(description='Book author'),
    'ID': fields.Integer(description='Book ID'),
    'Genre': fields.String(description='Book genre'),
    'Year_released': fields.Integer(description='year released'),
})


@api.route('/')
class ListBookOperations(Resource):
    def get(self, id):
        '''
        Returns list of books.
        '''
        #TODO: add get method, using query from db
        return books, 201

    @api.expect(book_model, validate=True)
    def post(self):
        '''
        Creates a new book.
        '''
        data = request.json
        return None, 204

@api.route('/genre/<string:genre>')
@api.doc(params={'genre': 'The genre for a list of books'})
class GenreBookOperations(Resource):
    def get(self, genre):
        '''

        Returns a list of books from the specific genre
        '''


@api.route('/book/<int:id>')
@api.doc(params={'id': 'An ID for a book'})
@api.doc(params={'Title': 'The title for the book'})
@api.doc(params={'Author': 'The author of the book'})
@api.doc(params={'Genre': 'The genre of the book'})
@api.doc(params={'YearReleased': 'The year the book was released'})
@api.doc(params={'CheckedOut': 'Whether the book is checked out'})
class BookOperations(Resource):
    def get(self, id):
        '''
        Returns a specific book.
        '''
        #TODO: add get method, using query from db
        return books, 201

    def put(self, id):
        '''

        Updates a book
        '''
        return None, 201

    def delete(self, id):
        '''
        Deletes a book.
        '''
        #TODO: create delete_book method
        return None, 204

