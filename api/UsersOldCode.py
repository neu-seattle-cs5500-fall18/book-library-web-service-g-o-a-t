from flask_restplus import Resource, Namespace, fields, reqparse


api = Namespace('Users', description='Operations related to users')

user_model = api.model('User', {
    'id': fields.Integer(readOnly=True, description= 'The unique identifier of a user'),
    'Name': fields.String(required=True, description = 'The name of a user')
})



#parser = reqparse.RequestParser()
#parser.add_argument('id', required=False)
#parser.add_argument('Name', required=False)

class User:
    def __init__(self, name, ID, comments):
        self.name = name
        self.ID = ID
        self.comments = comments
        self.deleted = False


users = []

@api.response(202, 'Accepted')
@api.response(404, 'Could not find any users')
@api.route('/')
class UserCollection(Resource):
    # TO-DO: add marshalling to get only specific fields
    def get(self):
        '''
            Return a list of users
            '''

        # TO-DO: create querying for list of users using db
        return users

    @api.response(404, 'Could not create a new user')
    @api.expect(user_model, validate=True)
    def post(self, id):
        """

            Creates a new user.

            """
        return users


@api.response(404, 'Could not get that specific user')
@api.route('/user/<int:id>')
@api.doc(params={'id': 'An ID for a user'})
class UserOperations(Resource):
    def get(self, id):
        """

            Returns a specific user.

            """
        #TODO: add get method, using query from db
        return users,

    @api.response(404, 'Could not update current user')
    def put(self, id):
        '''

        Updates a current user

        '''
        return None


    @api.response(202, 'User successfully deleted.')
    @api.response(404, 'User could not be deleted')
    def delete(self, id):
        """

            Deletes a user
            .

            """
        #TODO: create delete_user method
        return None



