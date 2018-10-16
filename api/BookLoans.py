from flask_restplus import Resource, fields, Namespace

api = Namespace('BookLoans', description='Operations related to book loans')

bookLoans = []

book_loan_model = api.model('BookLoans', {
   'loanID': fields.Integer(readOnly=True, description='The loan ID number.'),
   'bookID': fields.Integer(readOnly=True, description='The book ID of the book that is checked out.'),
   'LoanerID': fields.Integer(required=True, description='The ID of the user who checked the book out.'),
   'CheckedOutDate': fields.String(readOnly=True, description='The checked out date.'),
   'ReturnDate': fields.String(readOnly=True, description='The return date.')
   })

@api.route('/')
class BookLoan(Resource):
   @api.response(200, "Successful!")
   @api.response(404, "The loans were not found")
   def get(self):
       '''

       A list of all books currently checkd out.
       '''
       return bookLoans, 200

@api.route('/<int:loanID>')
class BookLoan(Resource):
    @api.doc(params={'loanID': 'The loan ID'})
    @api.response(200, 'Successful!')
    @api.response(404, 'The loan was not found.')
    def get(self, loanID):
        '''

        Gets a current loan.

        '''
        return None, 200

    #TODO: change the input paramaters of put/create
    def put(self,loanID):
        '''

        Creates a new loan
        '''
        return None, 200

    @api.doc(params={'loanID': "The loan ID to be deleted"})
    @api.response(200, "Deleted successfully")
    @api.response(404, "Delete unsuccessful")
    def delete(self, loanID):
        '''

        Deletes a book loan.

        '''
        return None, 2000



