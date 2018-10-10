
from flask import Flask
from flask_restplus import Api, Resource

app = Flask(__name__)
api = Api(Person)


@app.route('/Person')
class Person:
    def __init__(person, name, ID, comments):
        Person.name = name
        Person.ID = ID
        Person.comments = comments

