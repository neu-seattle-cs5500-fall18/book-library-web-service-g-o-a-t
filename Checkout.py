from flask import Flask
from flask_restplus import Api, Resource
import time
from datetime import date, timedelta

app = Flask(__name__)
api = Api(app)

@app.route('/Checkout')
class Checkout:
    def __init__(self, ID, book, author, comments, checkout_length):
        self.ID = ID
        self.book = book
        self.person = author
        self.comments = comments
        self.start_date = date.today()
        self.due_date = self.start_date + timedelta(days=checkout_length)