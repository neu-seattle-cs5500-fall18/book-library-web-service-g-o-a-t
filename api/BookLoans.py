from flask import Flask, request, jsonify, abort
from flask_restplus import Api, Resource, marshal, fields, Namespace, reqparse
from api.SharedModel import db
import datetime
from api.Books import BookDAO
from api.Books import BookDbModel
from api.Users import Users, UserDAO

from flask_mail import Mail, Message


api = Namespace('BookLoans', description='Operations related to book loans')

parser = reqparse.RequestParser()
parser.add_argument('user_id', type=int)
parser.add_argument('book_id', type=int)

parser1 = reqparse.RequestParser()
parser1.add_argument('book_id', type=int)
parser1.add_argument('loaner_id', type=int)
parser1.add_argument('checkout_date', type=str)
parser1.add_argument('return_date', type=str)
parser1.add_argument('due_date', type=str)
parser1.add_argument('comments', type=str)


book_loan_model = api.model('loan', {
    'loan_id': fields.Integer(readOnly=True, required=True, description= 'The unique identifier of a book loan'),
    'book_id': fields.Integer(required=False, description = 'The unique identifier of a book within a loan'),
    'loaner_id': fields.Integer(readOnly=True, required=True, description= 'The unique identifier of the person associated with the loan'),
    'checkout_date': fields.String(readOnly=False, description='The date the book was checked out in YYYY/MM/DD format'),
    'return_date': fields.String(readOnly=False, description='The date the book should be returned in YYYY/MM/DD format'),
    'due_date': fields.String(readOnly=False, description='The date the book is due in YYYY/MM/DD format'),
    'comments': fields.String(readOnly=False, description='Notes regarding this loan. Limit 100 chars')
})

# Database model
class loans(db.Model):
    loan_id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer)
    loaner_id = db.Column(db.Integer, db.ForeignKey(Users.id))
    checkout_date = db.Column(db.DateTime, default = datetime.datetime.utcnow)
    return_date = db.Column(db.DateTime, default = None)
    due_date = db.Column(db.DateTime, default = datetime.datetime.utcnow)
    comments = db.Column(db.String, default = "")

# Book_Loan class
class book_loan(object):
    def __init__(self, loan_id, book_id, loaner_id, checkout_date, return_date, due_date, comments):
        self.loan_id = loan_id
        self.book_id = book_id
        self.loaner_id = loaner_id
        self.checkout_date = checkout_date
        self.return_date = return_date
        self.due_date = due_date
        self.comments = comments

# Book Loan DAO
class loan_DAO(object):
    def __init__(self):
        self.counter = 0

    def to_dic(self, sql_object):
        list_loans = []
        for i in sql_object:
            list_loans.append({"loan_id": i.loan_id, "book_id": i.book_id, "loaner_id": i.loaner_id,
                               "checkout_date": i.checkout_date, "return_date": i.return_date, "due_date": i.due_date, "comments": i.comments})
        return list_loans

    def retrieve_all_loans(self):
        all_loans = loans.query.all()
        # return self.to_dic(all_loans)
        return all_loans

    def store(self, loan):
        while db.session.query(loans.loan_id).filter_by(loan_id = self.counter).scalar() is not None:
            self.counter += 1

        new_loan_id = self.counter
        db_loan = loans(loan_id = new_loan_id, book_id = loan.book_id, loaner_id = loan.loaner_id,
                           checkout_date = loan.checkout_date, return_date = loan.return_date, comments = loan.comments)
        db.session.add(db_loan)
        db.session.commit()
        return new_loan_id

    def retrieveOne(self, input_loan_id):
        retrieval_loan = loans.query.filter_by(loan_id = input_loan_id).first()
        return retrieval_loan

    def retrieveByUser(self, user_id):
        list_loans = loans.query.filter_by(loaner_id = user_id).all()
        return list_loans

    def retrieveByBook(self, book_id):
        list_loans = loans.query.filter_by(book_id = book_id).all()

    def update(self, loan_id, updated_loan):
        old_record = self.retrieveOne(loan_id)
        # old_record.loan_id = updated_loan['loan_id']
        if updated_loan['book_id'] is not None:
            old_record.book_id = updated_loan['book_id']
        if updated_loan['loaner_id'] is not None:
            old_record.loaner_id = updated_loan['loaner_id']
        if updated_loan['checkout_date'] is not None:
            old_record.checkout_date = updated_loan['checkout_date']
        if updated_loan['return_date'] is not None:   
            old_record.return_date = updated_loan['return_date']
        if updated_loan['due_date'] is not None:
            old_record.due_date = updated_loan['due_date']
        if updated_loan['comments'] is not None:
            old_record.comments = updated_loan['comments']
        db.session.commit()
        return "Book Loan " + str(loan_id) + " has been updated!"

    def delete(self, loan_id):
        loan_to_delete = loans.query.filter_by(loan_id=loan_id).first()
        db.session.delete(loan_to_delete)
        db.session.commit()
        return "Book Loan " + str(loan_id) + " has been deleted!"


class Checkout_DAO(BookDAO):

    def __init__(self):
        self.counter = 0;

    def update_status(self, book_id, new_status):
         old_status = self.get_a_book(book_id)
         old_status.checked_out = new_status
         db.session.commit()


    def get_loan(self, user_id, book_id, loan_id):
        loan = loans.query.filter_by(book_id = book_id, loaner_id = user_id, loan_id = loan_id).first()
        return loan

    def store_loan(self, user_id, book_id):
        while db.session.query(loans.loan_id).filter_by(loan_id = self.counter).scalar() is not None:
            self.counter += 1

        new_loan_id = self.counter
        db_loan = loans(loan_id = new_loan_id, book_id = book_id, loaner_id = user_id, return_date = None, due_date = datetime.datetime.now() + datetime.timedelta(days=7), comments = "check_out")
        db.session.add(db_loan)
        db.session.commit()

    def update_loan(self, user_id, book_id, loan_id):
        old_loan = self.get_loan(user_id, book_id, loan_id)
        old_loan.return_date = datetime.datetime.now()
        old_loan.comments = "returned"
        db.session.commit()

    def checkout_a_book(self, user_id, book_id):
        if db.session.query(Users.id).filter_by(id=user_id).scalar() is not None and db.session.query(BookDbModel.id).filter_by(id=book_id).scalar() is not None:
            status = BookDbModel.query.with_entities(BookDbModel.checked_out).filter_by(id=book_id).first()
            if status == (False,):
                self.update_status(book_id, True)
                self.store_loan(user_id, book_id)
            else:
                api.abort(404, description = "book is not available")
        else:
            api.abort(404, description = "can't find user id or book id")

    def return_a_book(self, user_id, book_id, loan_id):
        if self.get_loan(user_id, book_id, loan_id).return_date is None:
            print(self.get_loan(user_id, book_id, loan_id).return_date)
            self.update_status(book_id, False)
            self.update_loan(user_id, book_id, loan_id)
        else:
            api.abort(404, description = "you either didn't provide valid ids or book has been returned already")




DAO = loan_DAO()
DAO_checkout = Checkout_DAO()


@api.response(202, 'Book Loans successfully retrieved')
@api.response(404, "Book Loan not founded")
@api.route('/')
class Book_Loan_Controller(Resource):
    @api.marshal_with(book_loan_model)
    def get(self):
        """Returns all of the loans"""
        return DAO.retrieve_all_loans(), 202

    @api.response(202, 'New Book Loan successfully created')
    @api.response(404, 'Error creating new Book Loan')
    @api.expect(parser1)
    def post(self):
        """Creates a new Book Loan (Optional method to manualy create loan if needed)"""
        data = parser1.parse_args()
        new_book_loan = book_loan(0, data['book_id'], data['loaner_id'], data['checkout_date'], data['return_date'], data['due_date'], data['comments'])
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

    @api.response(200, 'Book Loan successfully updated')
    @api.response(404, 'Could not update current loan')
    @api.expect(parser1)
    def put(self, loan_id):
        '''Updates a current loan (Optional method to manualy update loan if needed)'''
        a_updated_loan = parser1.parse_args()
        DAO.update(loan_id, a_updated_loan)
        return 'sucess', 200       

    @api.response(200, "Book Loan successfully deleted")
    @api.response(404, "Unable to delete Book Loan")
    def delete(self, loan_id):
        """Deletes a Book Loan"""
        loan_to_delete = DAO.retrieveOne(loan_id)
        if not loan_to_delete:
            abort(404, 'Invalid Loan ID')

        DAO.delete(loan_id)
        return "Book Loan " + str(loan_id) + " has been deleted", 200

@api.route('/checkout')
@api.response(202, 'Accepted')
@api.response(404, 'Could not update a book')
class CheckoutBook(Resource):
    @api.response(202, 'checkout Accepted')
    @api.response(404, 'checkout failed')
    @api.expect(parser)
    def post(self):
        '''
        checkout book.
        '''
        data = parser.parse_args()
        DAO_checkout.checkout_a_book(data['user_id'], data['book_id'])
        return 'sucess', 202
@api.route('/return/<int:loan_id>')
class ReturnBook(Resource):
    @api.response(200, 'return process success.')
    @api.response(404, 'return process fail')
    @api.expect(parser)
    def put(self, loan_id):
        ''' Return book'''
        a_updated_loan = parser.parse_args()
        DAO_checkout.return_a_book(a_updated_loan['user_id'], a_updated_loan['book_id'], loan_id)
        return 'sucess', 200

