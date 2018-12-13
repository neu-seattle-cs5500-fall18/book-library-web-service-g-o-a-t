from flask import Flask
from api import api
from api.SharedModel import db
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from flask_mail import Mail, Message
from api.BookLoans import api as loans_api
from api.BookLoans import loan_DAO
from api.Users import UserDAO
from api.Books import BookDAO
from flask_restplus import Api, Resource, marshal, fields, Namespace, reqparse


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://dbektwgbeeergd:7728b9b046fe3d9ca2fe131ab9195aa25dd9e01d23e1b2a793a4063ec88edfc3@ec2-23-23-80-20.compute-1.amazonaws.com:5432/d5mbf8bg43kuh8'
api.init_app(app)

mail=Mail(app)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'iheartjewart@gmail.com'
app.config['MAIL_PASSWORD'] = 'monishnaidu'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

loan_DAO = loan_DAO()
user_DAO = UserDAO()
book_DAO = BookDAO()
@loans_api.route('/send reminder')
class Reminder(Resource):
    def get(self):
        """Send e-mail reminders to loaners"""
        for loan in loan_DAO.retrieve_all_loans():
            if loan.return_date is None:
                a_user = user_DAO.get_a_user(loan.loaner_id)
                a_user.notified = True
                db.session.commit()
                a_book = book_DAO.get_a_book(loan.book_id)
                msg = Message('Dear ' + a_user.name, sender = 'iheartjewart@gmail.com', recipients = [a_user.email])
                msg.body = "Just a reminder you checked out "+ a_book.title + " on " + str(loan.checkout_date) + ", you need to return your book by " + str(loan.due_date)
                mail.send(msg)
        return "emails Sent"



migrate = Migrate(app, db)

with app.app_context():
    db.init_app(app)
    db.create_all() # create table

if __name__ == '__main__':
    app.run()  # starting a development server



