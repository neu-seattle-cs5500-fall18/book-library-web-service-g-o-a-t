from flask import Flask, request
from flask_restplus import Resource, Namespace, fields, reqparse
from .SharedModel import db
api = Namespace('Books', description='Operations related to books')

books = []






# Api model
book_api_model = api.model('Book', {
    'title': fields.String(description='Book title'),
    'author': fields.String(description='Book author'),
    'id': fields.Integer(description='Book ID'),
    'genre': fields.String(description='Book genre'),
    'year_released': fields.String(description='year released'),
    'checked_out': fields.Boolean(description ='Is the book checked out'),
    'user_notes': fields.String(description = 'notes from user'),
})

#Input query processor for our get method
parser = reqparse.RequestParser()
parser.add_argument('title', required=False)
parser.add_argument('author', required=False)
parser.add_argument('genre', required=False)
parser.add_argument('year_released', required=False)
parser.add_argument('checked_out', required=False)

#Book class for python
class Book(object):
    def __init__(self, title, author, id, genre, year_released, checked_out, user_notes):
        self.title = title
        self.author = author
        self.id = id
        self.genre = genre
        self.year_released = year_released
        self.checked_out = checked_out
        self.user_notes = user_notes

#Database model for books
class BookDbModel (db.Model):
    title = db.Column(db.String(100))
    author = db.Column(db.String(100))
    id = db.Column(db.Integer, primary_key=True)
    genre = db.Column(db.String(100))
    year_released = db.Column(db.String(100))
    checked_out = db.Column(db.Boolean, default=False)
    user_notes = db.Column(db.String(100))

#Book DAO
class BookDAO(object):
    def __init__(self):
        self.counter = 0

    def to_dic(self, sql_object):
        my_list = []
        for book in sql_object:
            my_list.append({"title": book.title, "author": book.author, "id": book.id, "genre": book.genre, "year_released": book.year_released, "checked_out": book.checked_out, "user_notes": book.user_notes})
        return my_list

    def get_all_books(self):
        all_books = BookDbModel.query.all()
        return self.to_dic(all_books)

    def store(self, new_book):
        while db.session.query(BookDbModel.id).filter_by(id=self.counter).scalar() is not None:
            self.counter = self.counter + 1

        new_book.id = self.counter
        query = BookDbModel(title=new_book.title, author=new_book.author, id= new_book.id, genre=new_book.genre,year_released=new_book.year_released, checked_out= new_book.checked_out, user_notes=new_book.user_notes)
        db.session.add(query)
        db.session.commit()
        return new_book

    def get_a_book(self, book_id):
        a_book = BookDbModel.query.filter_by(id=book_id).first()
        return a_book

    def update(self, book_id, updated_book):
        old_book = self.get_a_book(book_id)
        if not old_book:
            api.abort(404)

        old_book.title = updated_book['title']
        old_book.author = updated_book['author']
        old_book.author = updated_book['genre']
        old_book.author = updated_book['year_released']
        old_book.checked_out = updated_book['checked_out']
        old_book.user_notes = updated_book['user_notes']
        db.session.commit()

    def delete(self, book_id):
        deleted_book = self.get_a_book(book_id)
        if not deleted_book:
            api.abort(404)
        db.session.delete(deleted_book)
        db.session.commit()

    def changeCheckOut(self, book_id, status):
        single_book = BookDbModel.query.filter_by(id=book_id).first()
        single_book.checked_out = status
        db.session.commit()



DAO = BookDAO()









@api.route('/')
@api.response(202, 'Accepted')
@api.response(404, 'Could not get a list of books')
class BooksController(Resource):

    # @api.expect(parser)
    def get(self):
        '''
        Returns list of books from given parameter.
        '''
        return DAO.get_all_books(), 202

        # return None

    @api.response(202, 'Accepted')
    @api.response(404, 'Could not create a new book')
    @api.expect(book_api_model)
    def post(self):
        '''
        Creates a new book.
        '''
        data = request.json
        new_book= Book(data['title'], data['author'], data['id'], data['genre'], data['year_released'],data['checked_out'], data['user_notes'])
        DAO.store(new_book)
        return 'sucess', 202



@api.response(202, 'Accepted')
@api.response(404,'ID does not exist')
@api.route('/book/<int:id>')

class BookController(Resource):
    @api.response(404, 'Could not get specific book')
    @api.marshal_with(book_api_model)
    def get(self, id):
        '''
        Returns a specific book.
        '''
        book = DAO.get_a_book(id)
        if not book:
            api.abort(404)
        else:
            return book

    @api.response(404, "could not update book")
    @api.expect(book_api_model)
    def put(self, id):
        '''

        Updates a book
        '''
        updated_book = request.json
        DAO.update(id, updated_book)
        return 'success', 200

    @api.response(404, "could not delete book")
    def delete(self, id):
        '''
        Deletes a book.
        '''
        DAO.delete(id)
        return 'Book deleted successfully', 200

