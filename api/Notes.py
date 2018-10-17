from flask_restplus import fields


class Notes:
    def __init__(self,book_name, book_id, notes):
        self.book_name = book_name
        self.book_id = book_id
        self.notes = notes



notes_model = api.model("Notes", {
    'book_name': fields.String(description='name of book'),
    'book_id': fields.Integer(description='Book ID'),
    'notes': fields.String(description='notes from the user regarding the book'),
})