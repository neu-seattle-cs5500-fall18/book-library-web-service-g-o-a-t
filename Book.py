from flask import Flask
from flask_restplus import Api, Resource, fields
from Serializers import book_model, user_model, app, api

ns = api.namespace('Collections', description='Operations related to books')

books = []

@ns.route('/User')
class book_collection(Resource):
        # TO-DO: add marshalling to get only specific fields

    def get(self):
        '''
        Return a list of Users
        '''

        # TO-DO: create querying for list of books using db
        return books, 201

@ns.route('/Book')
class book_operations(Resource):
    def get(self, id):
        '''
        Returns list of books.
        '''
        # TO-DO: add get method, using query from db
        return books, 201

    #@api.make_response(204, 'Book succesfully created.')
    #@api.expect(book_model)
    def put(self, id):
        '''
        Creates a new book.
        '''
        return books, 204

    #@api.response(204, 'Book successfully deleted.')
    #@api.expect(book_model)
    def delete(self, id):
        '''
        Deletes a book.
        '''
        # TO-DO: create delete_book method
        return None, 204

if __name__ == '__main__':
    app.run(debug = True)  #starting a development server