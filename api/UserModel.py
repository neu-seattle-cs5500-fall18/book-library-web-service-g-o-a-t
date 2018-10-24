import random
from flask import Flask
from flask_restplus import Namespace, Resource, fields
from werkzeug.contrib.fixers import ProxyFix
from api.SharedModel import db
from sqlalchemy import desc
#from .__init__ import app
#app = Flask(__name__) 
#app.wsgi_app = ProxyFix(app.wsgi_app)
#api = Api('user_list', title='UserList', version='2.0', description='user_list')

api = Namespace('Users', description='Operations related to users')

user_model = api.model('User', {
    'id': fields.Integer(readOnly=True, description= 'The unique identifier of a user'),
    'name': fields.String(required=True, description = 'The name of a user'),
    'deleted': fields.Boolean(required = False, description = 'deleted or not'),
    'comments': fields.String(required = True, description = 'comments about books?')
})

#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/librarytest'
#db = SQLAlchemy(app)

class Users(db.Model):
    ID = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80))
    deleted = db.Column(db.Boolean, default = False)
    comments = db.Column(db.String(80))

class User(object):
    def __init__(self, name, ID, comments):
        self.name = name
        self.ID = ID
        self.comments = comments
        self.deleted = False

class UserDAO(object):
    def __init__(self):
       self.counter = 0
       self.user_list = []

    def create(self, data):
        db.create_all();
        new_user = data
        while db.session.query(Users.ID).filter_by(ID = self.counter).scalar() is not None:
            self.counter = self.counter + 1
        new_user['id'] = self.counter
        self.user_list.append(new_user)
        
        query = Users(ID = new_user['id'], name = new_user['name'], deleted = new_user['deleted'], comments = new_user['comments'])
        db.session.add(query)
        db.session.commit()
        db.session.close()
        return new_user
    def get(self, id):
        for user in self.user_list:
            if user['id'] == id:
                return user
        api.abort(404, "user {} doesn't exist".format(id))

    def update(self, id, data):
        user = self.get(id)
        user.update(data)
        return user

    def delete(self, id):
        user = self.get(id)
        self.user_list.remove(user)

DAO = UserDAO()
#DAO.create({'name': 'Sally', 'deleted': False, 'comments': 'i dont know'})
@api.response(202, 'Accepted')
@api.response(404, 'Could not find any users')
@api.route('/')
class UserCollection(Resource):
    # TO-DO: add marshalling to get only specific fields
    api.marshal_list_with(user_model)
    def get(self):
        ''' Return a list of users'''
        return DAO.user_list

    @api.response(404, 'Could not create a new user')
    @api.expect(user_model)
    @api.marshal_with(user_model, code=202)
    def post(self):
        '''Creates a new user.'''
        return DAO.create(api.payload), 202

@api.response(404, 'Could not get that specific user')
@api.route('/<int:id>')
@api.doc(params={'id': 'An ID for a user'})
class UserOperations(Resource):
    @api.doc('get_user_list')
    @api.marshal_with(user_model)
    def get(self, id):
        '''Return a certain user'''
        return DAO.get(id)


    @api.response(404, 'Could not update current user')
    @api.expect(user_model)
    @api.marshal_with(user_model)
    def put(self, id):
        '''

        Updates a current user

        '''
        return DAO.update(id, api.payload)


    @api.response(202, 'User successfully deleted.')
    @api.response(404, 'User could not be deleted')
    @api.marshal_with(user_model)
    def delete(self, id):
        '''Deletes a user'''
        #TODO: create delete_user method
        DAO.delete(id)
        return '', 204


#if __name__ == '__main__':
#    app.run()



