from flask_restplus import Resource, Namespace, fields


ns = Namespace('BookList', description='Operations related to books')

books = []
book_model = ns.model("Book", {
    'Title': fields.String(description='Book title'),
    'Author': fields.String(description='Book author'),
    'ID': fields.Integer(min=1),
    'Genre': fields.String(description='Book genre'),
    'Year_released': fields.Integer(min=0),
    'Checked_out': fields.boolean(False),
})



@ns.route('/')
class ListBookOperations(Resource):
    def get(self, id):
        '''
        Returns list of books.
        '''
        # TO-DO: add get method, using query from db
        return books, 201


@ns.route('/book/<int:id>')
class BookOperations(Resource):
    def get(self, id):
        '''
        Returns a specific book.
        '''
        # TO-DO: add get method, using query from db
        return books, 201

    # @api.make_response(204, 'Book succesfully created.')
    # @api.expect(book_model)
    def put(self, id):
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
        # TO-DO: create delete_book method
        return None, 204

