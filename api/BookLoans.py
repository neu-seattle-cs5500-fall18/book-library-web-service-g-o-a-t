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


@api.response(202, 'Accepted')
@api.response(404, 'Could not do successfully')
@api.route('/')
class BookLoan(Resource):


   @api.response(404, "The loans were not found")
   def get(self):
       '''

       A list of all books currently checkd out.
       '''
       return bookLoans

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



