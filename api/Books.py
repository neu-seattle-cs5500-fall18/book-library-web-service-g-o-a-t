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
    'ID': fields.Integer(min=1),
    'Genre': fields.String(description='Book genre'),
    'Year_released': fields.Integer(min=0),
    'Checked_out': fields.boolean(False),
})

@api.route('/')
class ListBookOperations(Resource):
    def get(self, id):
        '''
        Returns list of books.
        '''
        #TODO: add get method, using query from db
        return books, 201

@api.route('/genre/<string:genre>')
@api.doc(params={'genre': 'The genre for a list of books'})
class GenreBookOperations(Resource):
    def get(self, genre):
        '''

        Returns a list of books from the specific genre
        '''


@api.route('/book/<int:id>')
@api.doc(params={'id': 'An ID for a book'})
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

    # @api.make_response(204, 'Book succesfully created.')
    # @api.expect(book_model)
    def post(self, id):
        '''
        Creates a new book.
        '''
        return books, 204

    # @api.response(204, 'Book successfully deleted.')
    # @api.expect(book_model)
    def delete(self, id):
        '''
        Deletes a book.
        '''
        #TODO: create delete_book method
        return None, 204

