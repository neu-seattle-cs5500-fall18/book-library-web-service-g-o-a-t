
from flask import Flask
from flask_restplus import Api, Resource

app = Flask(__name__)
api = Api(app)


@app.route('/Book')
class Book:
    def __init__(title, name, ID):
    	Book.title = title
        Book.name = name
        Book.ID = ID
