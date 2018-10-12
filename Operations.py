from flask import Flask, Blueprint
from flask_restplus import Api, Resource, fields
import Book

app = Flask(__name__)
api = Api(app) #doc=False

app.config['SWAGGER_UI_JSONEDITOR'] = True

book1 = Book.Book(1, "Hunger Game", "Jennifer", "action", 2012, "Nov")
book2 = Book.Book(2, "Harry Potter", "JK", "Fiction", 2000, "Dec")

# This is just a sample list to test out functionality
sample_library = [book1.title, book2.title]

#define book model
book_model = api.model("book", {"name": fields.String("Name of the book.")})

checkout = [book1, book2]

@api.route('/book')
class Book_operation(Resource):
	def get(self):
		return checkout

	@api.expect(book_model)
	def post(self):
		new_book = api.payload
		if new_book['name'] in sample_library:
			checkout.append(new_book)
			return {'result' : 'book has been added'}, 201
		else:
			return {'cannot find this book' : 'nothing is added'}, 404
	
	@api.expect(book_model)
	def delete(self):
		new_book = api.payload
		for book in checkout:
			if book["name"] == new_book["name"]:
				checkout.remove(book)
				return {'result' : 'book has been deleted'}, 204
		return {'cannot find this book': 'nothing is deleted'}, 404

if __name__ == '__main__':
    app.run(debug=True)
