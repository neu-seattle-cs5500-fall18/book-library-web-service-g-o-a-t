
#from flask import Flask
#from flask_restplus import Api, Resource

#app = Flask(__name__)
#api = Api(app)


#@app.route('/Book')
class Book:
    def __init__(self, ID, title, author, genre, year_released, checked_out):
        self.title = title
        self.author = author
        self.ID = ID
        self.genre = genre
        self.year_released = year_released
        self.checked_out = checked_out
        self.deleted = False
