from flask import Flask, request, jsonify
from flask_restplus import Api, Resource, marshal, fields, fields, Namespace
from random import randint
from flask_sqlalchemy import SQLAlchemy
from werkzeug.contrib.fixers import ProxyFix
from api.SharedModel import db

api = Namespace('BookLoans', description='Operations related to book loans')


app = Flask(__name__)
parser = api.parser()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ec2-23-23-80-20.compute-1.amazonaws.com:5432/d5mbf8bg43kuh8'
db = SQLAlchemy(app)


book_loan_model = api.model('loan', {
    'loan_id': fields.Integer(readOnly=True, required=True, description= 'The unique identifier of a book loan'),
    'book_id': fields.Integer(readOnly=True, required=True, description= 'The unique identifier of a book within the loan'),
    'loaner_id': fields.Integer(readOnly=True, required=True, description= 'The unique identifier of the person associated with the loan'),
    'checkout_date': fields.String(readOnly=False, description='The date the book was checked out in String format'),
    'return_date': fields.String(readOnly=False, description='The date teh book should be returned in String format'),
    'comments': fields.String(readOnly=False, description='Notes regarding this loan')
})

update_model = api.model('update book loan', {
    'loan_id': fields.Integer(required=True, description = 'The unique identifier of a book loan'),
    'book_id': fields.Integer(required=False, description = 'The unique identifier of a book within a loan'),
    'loaner_id': fields.Integer(required=False, description = 'The identifier of the person associated with the loan'),
    'checkout_Date': fields.String(required=False, description= 'The date the book was checked out in String format'),
    'return_date': fields.String(required=False, description='The date the book should be returned in String format'),
    'comments': fields.String(required=False, description='Notes regarding this loan')
})

# Database model
class loans(db.model):
    loan_id = db.column(db.Integer, primary_key=True)
    book_id = db.column(db.Integer)
    loaner_id = db.column(db.Integer)
    checkout_date = db.column(db.String, default = "")
    return_date = db.column(db.String, default = "")
    comments = db.column(db.String, default = "")

# Book_Loan class
class book_loan(object):
    def __init_(self, loan_id, book_id, loaner_id, checkout_date, return_date, comments):
        self.loan_id = loan_id
        self.book_id = book_id
        self.loaner_id = loaner_id
        self.checkout_date = checkout_date
        self.return_date = return_date
        self.comments = comments

# User DAO
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
        if not old_record:
            api.abort(404)
        old_record.loan_id = updated_loan.loan_id
        old_record.book_id = updated_loan.book_id
        old_record.loaner_id = updated_loan.loaner_id
        old_record.checkout_date = updated_loan.checkout_date
        old_record.return_date = updated_loan.return_date
        old_record.comments = updated_loan.comments
        db.session.commit()
        return "Book Loan " +str(loan_id) + " has been updated!"

    def delete(self, loan_id):

        loan_to_delete = loans.query.filter(loanid=loan_id).first()

        if loan_to_delete is None:
            return "Invalid game ID"

        db.session.delete(loan_to_delete)
        db.session.commit()
        return "Book Loan " + str(loan_id) + " has been deleted!"




DAO = loan_DAO()

@api.response(202, 'Book Loans successfully retrieved')
@api.response(404, "Book Loan not founded")
@api.route('/')
class Book_Loan_Collection(Resource):
    """Returns all of the loans"""
    def get(self):
        return DAO.retrieve_all_loans(), 202

    @api.response(202, 'New Book Loan successfully created')
    @api.response(404, 'Error creating new Book Loan')
    @api.expect(book_loan_model)
    def post(self):
        """Creates a new Book Loan"""
        data = request.json
        new_book_loan = book_loan(data["loan_id"], data['book_id'], data['user_id'],
                                  data['checkout date'], data["return date"], data['comments'])
        DAO.store(new_book_loan)
        return 'Sucessfuly created new Book Loan', 202


@api.route('/<int:loan_id')
class Book_Loan_Operations(Resource):
    @api.response(200, 'Book Loan successfully obtained')
    @api.response(404, 'Unable to retrieve book loan')
    @api.marshal(book_loan_model)
    def get(self, loan_id):
        """Retrieves a single loan from a loan id"""
        single_loan = DAO.retrieveOne(loan_id)
        if not single_loan:
            api.abort(404)
        else:
            return single_loan, 200

    def get(self, user_id):
        loans_for_user = DAO.retrieveByUser(user_id)
        if not loans_for_user:
            api.abort(404)
        else:
            return loans_for_user, 200

    def get(self, book_id):
        loans_for_book = DAO.retrieveByBook(book_id)
        if not loans_for_book:
            api.abort(404)
        else:
            return loans_for_book, 200

    def put(self, loan_id):
        updated_loan = request.json
        DAO.update(loan_id, updated_loan)
        return "Successfully updated", 200

    @api.response(200, "Book Loan successfully deleted")
    @api.response(404, "Unable to delete Book Loan")
    def delete(self, loan_id):
        """Deletes a Book Loan"""
        DAO.delete(loan_id)
        return "Book Loan has been deleted", 200


""" Below this line is the old code

book_loan_model = api.model('BookLoans', {
   'loanID': fields.Integer(readOnly=True, description='The loan ID number.'),
   'bookID': fields.Integer(readOnly=True, description='The book ID of the book that is checked out.'),
   'LoanerID': fields.Integer(required=True, description='The ID of the user who checked the book out.'),
   'CheckedOutDate': fields.String(readOnly=True, description='The checked out date.'),
   'ReturnDate': fields.String(readOnly=True, description='The return date.'),
    'Notes': fields.String(readOnly=True, description='Extra comments about the loan')
   })


@api.response(202, 'Accepted')
@api.response(404, 'Could not do successfully')
@api.route('/')
class BookLoan(Resource):


   @api.response(404, "The loans were not found")
   def get(self):
       '''

       A list of all books currently checkd out.
       '''
       book_loans = []

       loans = db.query.all()

       for loan in loans:
           book_loans.append(loan)

       return jsonify(book_loans)

   # Makes body match book loans
   # TODO: change the input paramaters of put/create
   @api.expect(book_loan_model, validate=True)


   @api.response(201, 'Created a new loan')
   def post(self):
       '''

       Creates a new loan
       '''
       return None

@api.response(202, 'Successful!')
@api.response(404, 'Could not complete')
@api.route('/<int:loanID>')
class BookLoan(Resource):
    @api.doc(params={'loanID': 'The loan ID'})

    def get(self, loanID):
        '''

        Gets a current loan.

        '''
        return None

    def put(self, loanID):
        '''

        Updates a current loan
        '''
        return None




    @api.doc(params={'loanID': "The loan to be deleted"})
    @api.response(202, "Deleted successfully")
    @api.response(404, "Delete unsuccessful")
    def delete(self, loanID):
        '''

        Deletes a book loan.

        '''
        return None



"""