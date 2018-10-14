from flask import Flask, Blueprint
from flask_restplus import Api, Resource, fields


app = Flask(__name__)
api = Api(app)  # doc=False

app.config['SWAGGER_UI_JSONEDITOR'] = True  # puts josn editor in swagger ui (TO-DO: doesn't seem to work)


# This is just a sample list to test out functionality
# sample_library = [book1.title, book2.title]

# temporary book database
books = []



# define book model


book_model = api.model("book", {"Title": fields.String("Name of the book.")})



@api.route('/book/<int:id>')
class Book_operation(Resource):
    def get(self):
        return books

    @api.expect(book_model)  # decorator (expect that takes in a book_model)
    def post(self):
        new_book = api.payload  # the payload (json object) received from the client
        books.append(new_book)
        return {'result': 'Book added successfully'}, 201

    @api.expect(book_model)
    def delete(self):
        # Deletes book
        return None, 204

    # new_book = api.payload
    # for book in checkout:
    #    if book["name"] == new_book["name"]:
    #       checkout.remove(book)
    #      return {'result': 'book has been deleted'}, 204
    # return {'cannot find this book': 'nothing is deleted'}, 404

# if __name__ == '__main__':
#   app.run(debug=True)
