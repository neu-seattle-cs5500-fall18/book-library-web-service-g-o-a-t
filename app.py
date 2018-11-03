from flask import Flask
from api import api
from api.SharedModel import db
from flask_sqlalchemy import SQLAlchemy
#put some comments: Jimmy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://dbektwgbeeergd:7728b9b046fe3d9ca2fe131ab9195aa25dd9e01d23e1b2a793a4063ec88edfc3@ec2-23-23-80-20.compute-1.amazonaws.com:5432/d5mbf8bg43kuh8'
api.init_app(app)

with app.app_context():
    db.init_app(app)
    db.create_all() # create table

if __name__ == '__main__':
    app.run()  # starting a development server
