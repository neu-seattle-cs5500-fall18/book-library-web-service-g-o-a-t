from flask import Flask
from flask_restplus import Api, Resource, fields
from Serializers import book_model

app = Flask(__name__)
api = Api(app)

ns = api.namespace('books', description='Operations related to individual books')

# define book model

books = []


class Book:
    def __init__(self, ID, title, author, genre, year_released, checked_out):
        self.title = title
        self.author = author
        self.ID = ID
        self.genre = genre
        self.year_released = year_released
        self.checked_out = checked_out
        self.deleted = False

    @ns.route('/')
    class BookCollection(Resource):
        # TO-DO: add marshalling to get only specific fields
        def get(self):
            return books, 201

    @api.route('/book/<int:id>')
    class Book_operation(Resource):
        def get(self, id):
            '''

            Returns list of books.

            '''
            # TO-DO: add get method, using query from db
            return books, 201

        @api.make_response(201, 'Book successfully created.')
        @api.expect(book_model)  # decorator (expect that takes in a book_model)
        def post(self):
            # Creates a new book
            return None, 201

        @api.expect(book_model)
        def delete(self, id):
            # Deletes book
            return {'result': 'Book deleted successfully'}, 204
