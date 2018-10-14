
from flask import Flask
from flask_restplus import Api, Resource, fields

app = Flask(__name__)
api = Api(app)

# define book model
book_model = api.model('Book', {
    'Title': fields.String(description='Book title'),
    'Author': fields.String(description='Book author'),
    'ID': fields.Integer(min=1),
    'Genre': fields.String(description='Book genre'),
    'Year_released': fields.Integer(min=0),
    'Checked_out': fields.boolean(False),
})


#@app.route('/Book')
class Book:
    def __init__(self, ID, title, author, genre, year_released, checked_out):
        self.title = title
        self.author = author
        self.ID = ID
        self.genre = genre
        self.year_released = year_released
        self.checked_out = checked_out
        self.deleted = False

    @api.route('/book/<int:id>')
    class Book_operation(Resource):
        def get(self,id):
            return Book

        @api.expect(book_model)  # decorator (expect that takes in a book_model)
        def post(self,id):
            #update book
            new_book = api.payload  # the payload (json object) received from the client
            return {'result': 'Book updated successfully'}, 201

        @api.expect(book_model)
        def delete(self,id):
            # Deletes book
            return {'result': 'Book deleted successfully'}, 204

