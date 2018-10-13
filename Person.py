
from flask import Flask
from flask_restplus import Api, Resource

app = Flask(__name__)
api = Api(app)


@app.route('/Person')
class Person:
    def __init__(self, name, ID, comments):
        self.name = name
        self.ID = ID
        self.comments = comments
        self.deleted = False


