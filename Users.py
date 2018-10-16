from flask import Flask
from flask_restplus import Api, Resource, fields
from Serializers import user_model

app = Flask(__name__)
api = Api(app)

ns = api.namespace('Collections', description='Operations related to users')


class Person:
    def __init__(self, name, ID, comments):
        self.name = name
        self.ID = ID
        self.comments = comments
        self.deleted = False


users = []


@ns.route('/')
class UserCollection(Resource):
    # TO-DO: add marshalling to get only specific fields

    def get(self):
        '''
            Return a list of users
            '''

        # TO-DO: create querying for list of users using db
        return users, 201


@ns.route('/user/<int:id>')
class UserOperations(Resource):
    def get(self, id):
        '''

            Returns list of users.

            '''
        # TO-DO: add get method, using query from db
        return users, 201

    @ns.make_response(204, 'User successfully created.')
    @ns.expect(user_model)
    def put(self, id):
        '''

            Creates a new user.

            '''
        return users, 204

    @ns.response(204, 'User successfully deleted.')
    def delete(self, id):
        '''

            Deletes a user
            .

            '''
        # TO-DO: create delete_user method
        return None, 204
