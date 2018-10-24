from flask import Flask
from api import api
from api.SharedModel import db
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/librarytest'
api.init_app(app)

with app.app_context():
    db.init_app(app)


if __name__ == '__main__':
    app.run()  # starting a development server
