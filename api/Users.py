from flask_restplus import Resource, Namespace, fields


api = Namespace('Users', description='Operations related to users')

user_model = api.model('User', {
    'id': fields.Integer(readOnly=True, description= 'The unique identifier of a user'),
    'Name': fields.String(required=True, description = 'The name of a user')
})
class User:
    def __init__(self, name, ID, comments):
        self.name = name
        self.ID = ID
        self.comments = comments
        self.deleted = False


users = []


@api.route('/')
class UserCollection(Resource):
    # TO-DO: add marshalling to get only specific fields
    def get(self):
        '''
            Return a list of users
            '''

        # TO-DO: create querying for list of users using db
        return users, 201


@api.route('/user/<int:id>')
@api.doc(params={'id': 'An ID for a user'})
class UserOperations(Resource):
    def get(self, id):
        """

            Returns a specific user.

            """
        #TODO: add get method, using query from db
        return users, 201


    @api.expect(user_model)
    def put(self, id):
        '''

        Updates a current user

        '''
        return None, 204

    def post(self, id):
        """

            Creates a new user.

            """
        return users, 204

    @api.response(204, 'User successfully deleted.')
    def delete(self, id):
        """

            Deletes a user
            .

            """
        #TODO: create delete_user method
        return None, 204
