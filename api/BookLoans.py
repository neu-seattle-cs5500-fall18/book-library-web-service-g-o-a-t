from flask import Flask, request, jsonify, abort
from flask_restplus import Api, Resource, marshal, fields, fields, Namespace
from random import randint
from flask_sqlalchemy import SQLAlchemy
from werkzeug.contrib.fixers import ProxyFix
from api.SharedModel import db
from datetime import time, datetime, date, timedelta
from api.DateTime import valid_date, string_to_date, check_valid_timediff
from api.Books import BookDAO
from api.UserModel import UserDAO

api = Namespace('BookLoans', description='Operations related to book loans')


app = Flask(__name__)
parser = api.parser()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ec2-23-23-80-20.compute-1.amazonaws.com:5432/d5mbf8bg43kuh8'
db = SQLAlchemy(app)






book_loan_model = api.model('loan', {
    'loan_id': fields.Integer(readOnly=True, required=True, description= 'The unique identifier of a book loan'),
    'book_id': fields.Integer(readOnly=True, required=True, description= 'The unique identifier of a book within the loan'),
    'loaner_id': fields.Integer(readOnly=True, required=True, description= 'The unique identifier of the person associated with the loan'),
    'checkout_date': fields.String(readOnly=False, description='The date the book was checked out in YYYY/MM/DD format'),
    'return_date': fields.String(readOnly=False, description='The date the book should be returned in YYYY/MM/DD format'),
    'comments': fields.String(readOnly=False, description='Notes regarding this loan. Limit 100 chars')
})

update_model = api.model('update book loan', {
    'loan_id': fields.Integer(required=True, description = 'The unique identifier of a book loan'),
    'book_id': fields.Integer(required=False, description = 'The unique identifier of a book within a loan'),
    'loaner_id': fields.Integer(required=False, description = 'The identifier of the person associated with the loan'),
    'checkout_Date': fields.String(required=False, description= 'The date the book was checked out in YYYY/MM/DD format'),
    'return_date': fields.String(required=False, description='The date the book should be returned in YYYY/MM/DD format'),
    'comments': fields.String(required=False, description='Notes regarding this loan. Limit 100 chars')
})

# Database model
class loans(db.Model):
    loan_id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer)
    loaner_id = db.Column(db.Integer)
    checkout_date = db.Column(db.String, default = "")
    return_date = db.Column(db.String, default = "")
    comments = db.Column(db.String, default = "")

# Book_Loan class
class book_loan(object):
    def __init_(self, loan_id, book_id, loaner_id, checkout_date, return_date, comments):
        self.loan_id = loan_id
        self.book_id = book_id
        self.loaner_id = loaner_id
        self.checkout_date = string_to_date(checkout_date)
        self.return_date = string_to_date(return_date)
        self.comments = comments

# Book Loan DAO
class loan_DAO():
    def __init__(self):
        self.counter = 0

    def to_dic(self, sql_object):
        list_loans = []
        for i in sql_object:
            list_loans.append({"loan_id": i.loan_id, "book_id": i.book_id, "loaner_id": i.loander_id,
                               "checkout_date": i.checkout_date, "return_date": i.return_date, "comments": i.comments})
        return list_loans

    def retrieve_all_loans(self):
        all_loans = loans.query.all()
        return self.to_dic(all_loans)

    def store(self, loan):
        while db.session.query.filter_by(loanid = self.counter).scalar() is not None:
            self.counter += 1

        new_loan_id = self.counter
        db_loan = loans(loanid = new_loan_id, bookid = loan.book_id, loanerid = loan.loaner_id,
                           checkoutdate = loan.checkout_date, returndate = loan.return_date, comments = loan.comments)
        db.session.add(db_loan)
        db.session.commit()
        return new_loan_id

    def retrieveOne(self, input_loan_id):
        retrieval_loan = loans.query.filter_by(loanid = input_loan_id).first()
        return retrieval_loan

    def retrieveByUser(self, user_id):
        list_loans = loans.query.filter_by(loanerid = user_id).all()
        return list_loans

    def retrieveByBook(self, book_id):
        list_loans = loans.query.filter_by(bookid = book_id).all()

    def update(self, loan_id, updated_loan):
        old_record = self.retrieveOne(loan_id)
        old_record.loan_id = updated_loan.loan_id
        old_record.book_id = updated_loan.book_id
        old_record.loaner_id = updated_loan.loaner_id
        old_record.checkout_date = updated_loan.checkout_date
        old_record.return_date = updated_loan.return_date
        old_record.comments = updated_loan.comments
        db.session.commit()
        return "Book Loan " + str(loan_id) + " has been updated!"

    def delete(self, loan_id):

        loan_to_delete = loans.query.filter(loanid=loan_id).first()
        db.session.delete(loan_to_delete)
        db.session.commit()
        return "Book Loan " + str(loan_id) + " has been deleted!"




DAO = loan_DAO()
DAO_Books = BookDAO()
DAO_Users = UserDAO()


@api.response(202, 'Book Loans successfully retrieved')
@api.response(404, "Book Loan not founded")
@api.route('/')
class Book_Loan_Controller(Resource):
    """Returns all of the loans"""
    def get(self):
        return DAO.retrieve_all_loans(), 202

    @api.response(202, 'New Book Loan successfully created')
    @api.response(404, 'Error creating new Book Loan')
    @api.expect(book_loan_model)
    def post(self):
        """Creates a new Book Loan"""
        data = request.json
        if not valid_date(data['checkout date']):
            return 'Date values for checkout date are not valid', 404
        if not  valid_date(data['return date']):
            return 'Date values for return date are not valid', 404
        if not check_valid_timediff(data['checkout date'], data['return date']):
            return 'return date cannot be before checkout date'


        """Still need to check that book_id is valid"""
        single_book = DAO_Books.get_a_book(data['book_id'])
        if not single_book:
            abort(404, 'Invalid book ID')

        """Still need to change book's checkout status"""
        DAO_Books.changeCheckOut(data['book_id'], True)

        """Still need to check that user_id is valid"""
        user = DAO_Users.get_a_user(data['user_id'])
        if not user:
            abort(404, 'Invalid user ID')


        new_book_loan = book_loan(data["loan_id"], data['book_id'], data['user_id'],
                                  data['checkout date'], data["return date"], data['comments'])
        DAO.store(new_book_loan)
        return 'Sucessfuly created new Book Loan', 202


@api.route('/<int:loan_id>')
class Book_Loan_Controller_Loan_ID(Resource):
    @api.response(200, 'Book Loan successfully obtained')
    @api.response(404, 'Unable to retrieve book loan')
    @api.marshal_with(book_loan_model)
    def get(self, loan_id):
        """Retrieves a single loan from a loan id"""
        single_loan = DAO.retrieveOne(loan_id)
        if not single_loan:
            abort(404, 'Invalid Loan ID')
        else:
            return single_loan, 200

    def get(self, user_id):
        loans_for_user = DAO.retrieveByUser(user_id)
        if not loans_for_user:
            abort(404, 'Invalid User ID')
        else:
            return loans_for_user, 200

    def get(self, book_id):
        loans_for_book = DAO.retrieveByBook(book_id)
        if not loans_for_book:
            abort(404, 'Invalid Book ID')
        else:
            return loans_for_book, 200

    def put(self, loan_id):
        updated_loan = request.json
        updated_loan = DAO.retrieveOne(loan_id)
        if not updated_loan:
            abort(404, 'Invalid Loan ID')
        else:
            DAO.update(loan_id, updated_loan)
            return "Successfully updated loan " + str(loan_id), 200

    @api.response(200, "Book Loan successfully deleted")
    @api.response(404, "Unable to delete Book Loan")
    def delete(self, loan_id):
        """Deletes a Book Loan"""


        """Still need to change Book's status from checkedout to NOT checkedout"""

        loan_to_delete = DAO.retrieveOne(loan_id)
        if not loan_to_delete:
            abort(404, 'Invalid Loan ID')

        DAO_Books.changeCheckOut(loan_to_delete.book_id, False)
        DAO.delete(loan_id)
        return "Book Loan " + str(loan_id) + " has been deleted", 200

