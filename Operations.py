from flask import Flask
from flask_restplus import Api, Resource, fields
import Book

app = Flask(__name__)
api = Api(app)

book1 = Book.Book(1, "Hunger Game", "Jennifer", "action", 2012, "Nov")
book2 = Book.Book(2, "Harry Potter", "JK", "Fiction", 2000, "Dec")

# This is just a sample list to test out functionality
sample_library = [book1.title, book2.title]

#define book model
book_model = api.model("book", {"name": fields.String("Name of the book.")})

checkout = []

@api.route('/book')
class Book_operation(Resource):
	def get(self):
		return checkout

	@api.expect(book_model)
	def post(self):
		new_book = api.payload
		if new_book['name'] in sample_library:
			checkout.append(new_book)
			return {'result' : 'book has been added'}
		else:
			return {'cannot find this book' : 'nothing is added'}
	
	@api.expect(book_model)
	def delete(self):
		new_book = api.payload
		for book in checkout:
			if book["name"] == new_book["name"]:
				checkout.remove(book)
				return {'result' : 'book has been deleted'}
		return {'cannot find this book': 'nothing is deleted'} 		

if __name__ == '__main__':
    app.run(debug=True)
