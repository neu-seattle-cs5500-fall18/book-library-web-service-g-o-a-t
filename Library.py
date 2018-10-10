from flask import Flask
from flask_restplus import Api, Resource

app = Flask(__name__)

api = Api(app)


@app.route('/Book')
class Library(object):
    def __init__(Library_Id, Books):
        Library.Library_Id = Library_Id
        Library.Books = Books




