from flask import Flask
from api import api
from api.SharedModel import db
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/librarytest'
api.init_app(app)


migrate = Migrate(app, db)

with app.app_context():
    db.init_app(app)
    db.create_all() # create table

if __name__ == '__main__':
    app.run()  # starting a development server

