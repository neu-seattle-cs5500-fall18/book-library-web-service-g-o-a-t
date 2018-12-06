from flask import Flask
from api import api
from api.SharedModel import db
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://dbektwgbeeergd:7728b9b046fe3d9ca2fe131ab9195aa25dd9e01d23e1b2a793a4063ec88edfc3@ec2-23-23-80-20.compute-1.amazonaws.com:5432/d5mbf8bg43kuh8'
api.init_app(app)
# mail = Mail(app)
#
# app.config['MAIL_SERVER']='smtp.gmail.com'
# app.config['MAIL_PORT'] = 465
# app.config['MAIL_USERNAME'] = 'iheartjewart@gmail.com'
# app.config['MAIL_PASSWORD'] = 'monishnaidu'
# app.config['MAIL_USE_TLS'] = False
# app.config['MAIL_USE_SSL'] = True
# mail = Mail(app)







migrate = Migrate(app, db)

with app.app_context():
    db.init_app(app)
    db.create_all() # create table

if __name__ == '__main__':
    app.run()  # starting a development server



