from flask import Flask, request
from flask_restplus import Namespace, Resource, fields, reqparse
from api.SharedModel import db

parser = reqparse.RequestParser()
parser.add_argument('name', type=str)
parser.add_argument('deleted', type=bool)
parser.add_argument('comments', type=str)


api = Namespace('Users', description='Operations related to users')

user_model = api.model('User', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of a user'),
    'name': fields.String(required=True, description='The name of a user'),
    'deleted': fields.Boolean(required=False, description='deleted or not'),
    'comments': fields.String(required=True, description='comments about books?'),
    'email': fields.String(required=True, description='The email associated with a user')
})


# Database model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    deleted = db.Column(db.Boolean, default=False)
    comments = db.Column(db.String(80))
    email = db.Column(db.String(80))


# User class
class User(object):
    def __init__(self, id, name, deleted, comments, email):
        self.id = id
        self.name = name
        self.deleted = False
        self.comments = comments
        self.email = email


# User DAO
class UserDAO(object):
    def __init__(self):
        self.counter = 0

    def to_dic(self, sql_object):
        my_list = []
        for i in sql_object:
            my_list.append({"id": i.id, "name": i.name, "deleted": i.deleted, "comments": i.comments, "email": i.email})
        return my_list

    def get_all_users(self):
        all_record = Users.query.all()
        return self.to_dic(all_record)

    def store(self, new_user):
        while db.session.query(Users.id).filter_by(id=self.counter).scalar() is not None:
            self.counter = self.counter + 1

        new_user.id = self.counter
        query = Users(id=new_user.id, name=new_user.name, deleted=new_user.deleted, comments=new_user.comments, email=new_user.email)
        db.session.add(query)
        db.session.commit()
        return new_user

    def get_a_user(self, user_id):
        a_user = Users.query.filter_by(id=user_id).first()
        return a_user

    def update(self, id, updated_user):
        old_record = self.get_a_user(id)
        if not old_record:
            api.abort(404)
        old_record.name = updated_user['name']
        old_record.deleted = updated_user['deleted']
        old_record.comments = updated_user['comments']
        db.session.commit()

    def delete(self, id):
        deleted_user = self.get_a_user(id)
        if not deleted_user:
            api.abort(404)
        db.session.delete(deleted_user)
        db.session.commit()

DAO = UserDAO()


@api.response(202, 'users successfully obtained')
@api.response(404, 'Could not find any users')
@api.route('/')
class UserCollection(Resource):
    def get(self):
        ''' Return a list of users'''
        return DAO.get_all_users(), 202

    @api.response(202, 'User successfully created')
    @api.response(404, 'Could not create a new user')
    @api.expect(parser)
    def post(self):
        '''Creates a new user.'''
        data = parser.parse_args()
        new_user = User(0, data['name'], data['deleted'], data['comments'], data['email'])
        DAO.store(new_user)
        return 'success', 202


@api.route('/<int:id>')
class UserOperations(Resource):
    @api.response(200, 'User successfully obtained')
    @api.response(404, 'Could not get that specific user')
    @api.marshal_with(user_model)
    def get(self, id):
        '''Return a certain user by id'''
        user = DAO.get_a_user(id)
        if not user:
            api.abort(404)
        else:
            return user, 200

    @api.response(200, 'User successfully updated.')
    @api.response(404, 'Could not update current user')
    @api.expect(parser)
    def put(self, id):
        ''' Updates a current user'''
        a_updated_user = parser.parse_args()
        DAO.update(id, a_updated_user)
        return 'sucess', 200

    @api.response(200, 'User successfully deleted.')
    @api.response(404, 'User could not be deleted')
    def delete(self, id):
        '''Deletes a user'''
        DAO.delete(id)
        return 'sucess', 200
