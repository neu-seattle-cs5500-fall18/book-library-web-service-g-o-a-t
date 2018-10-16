from flask import Flask
from flask_restplus import fields, Api
from .Users import api as user_api
from .Books import api as book_api

#TODO: add all the models to this page and import to other classes

app = Flask(__name__)
api = Api(app)

user_model = user_api.model('User', {
    'id': fields.Integer(readOnly=True, description= 'The unique identifier of a user'),
    'Name': fields.String(required=True, description = 'The name of a user')
})

book_model = book_api.model("Book", {
    'Title': fields.String(description='Book title'),
    'Author': fields.String(description='Book author'),
    'ID': fields.Integer(min=1),
    'Genre': fields.String(description='Book genre'),
    'Year_released': fields.Integer(min=0),
    'Checked_out': fields.boolean(False),
})

book_loan_model = api.model('BookLoans', {
   'loanID': fields.Integer(readOnly=True, description='The loan ID number.'),
   'bookID': fields.Integer(readOnly=True, description='The book ID of the book that is checked out.'),
   'LoanerID': fields.Integer(required=True, description='The ID of the user who checked the book out.'),
   'CheckedOutDate': fields.String(readOnly=True, description='The checked out date.'),
   'ReturnDate': fields.String(readOnly=True, description='The return date.')
   })
