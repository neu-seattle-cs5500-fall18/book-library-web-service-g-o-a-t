from flask import Flask
from flask_restplus import Api, Resource, fields
from Serializers import book_model

app = Flask(__name__)
api = Api(app)

ns = api.namespace('Collections', description='Operations related to books')


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
    class book_collection(Resource):
        # TO-DO: add marshalling to get only specific fields

        def get(self):
            '''
            Return a list of books
            '''

            # TO-DO: create querying for list of books using db
            return books, 201

    @api.route('/book/<int:id>')
    class book_operations(Resource):
        def get(self, id):
            '''

            Returns list of books.

            '''
            # TO-DO: add get method, using query from db
            return books, 201

        @api.make_response(204, 'Book succesfully created.')
        @api.expect(book_model)
        def put(self, id):
            '''

            Creates a new book.

            '''
            return books, 204

        @api.response(204, 'Book successfully deleted.')
        def delete(self, id):
            '''

            Deletes a book.

            '''
            # TO-DO: create delete_book method
            return None, 204
