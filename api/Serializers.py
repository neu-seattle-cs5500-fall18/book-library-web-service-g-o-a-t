from flask import Flask
from flask_restplus import fields, Api
from .Users import ns as user_api
from .Book import ns as book_api

app = Flask(__name__)
api = Api(app)

user_model = user_api.model('User', {
    'id': fields.Integer(readOnly=True, description= 'The unique identifier of a user'),
    'Name': fields.String(required=True, description = 'The name of a user')
})

book_model = book_api.model("Book", {
    'Title': fields.String(description='Book title'),
    'Author': fields.String(description='Book author'),
    'ID': fields.Integer(min=1),
    'Genre': fields.String(description='Book genre'),
    'Year_released': fields.Integer(min=0),
    'Checked_out': fields.boolean(False),
})
