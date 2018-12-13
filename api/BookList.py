from flask import Flask, request
from flask_restplus import Namespace, Resource, fields, reqparse
from api.SharedModel import db
from api.Books import BookDbModel
from api.Users import Users

parser = reqparse.RequestParser()
parser.add_argument('user_id', type=str)
parser.add_argument('list_name', type=str)
parser.add_argument('book_ids', action='append', type=int)
parser1 = reqparse.RequestParser()
parser1.add_argument('list_name', type=str)
parser1.add_argument('book_ids', action='append', type=int)

api = Namespace('BookList', description='Operations related to BookList')

list_model = api.model('List', {
    'list_id': fields.Integer(readOnly=True, description='The unique identifier of a list'),
    'list_name': fields.String(required=True, description='The name of a list'),
    'user_id': fields.Integer(required=False, description='an user id'),
    'book_ids': fields.List(fields.Integer(requried = False, descpriton = 'book ids'))
})


# Database model
class Lists(db.Model):
    list_id = db.Column(db.Integer, primary_key=True)
    list_name = db.Column(db.String(80))
    user_id = db.Column(db.Integer)
    book_ids = db.Column(db.ARRAY(db.Integer))

# User class
class List(object):
    def __init__(self, list_id, list_name, user_id, book_ids):
        self.list_id = list_id
        self.list_name = list_name
        self.user_id = user_id
        self.book_ids = book_ids

# User DAO
class ListDAO(object):
    def __init__(self):
        self.counter = 0

    def to_dic(self, sql_object):
        my_list = []
        for i in sql_object:
            my_list.append({"list_id": i.list_id, "list_name": i.list_name, "user_id": i.user_id, "book_ids": i.book_ids})
        return my_list

    def get_all_lists(self):
        all_record = Lists.query.all()
        return self.to_dic(all_record)

    def store(self, new_list):
        self.validate_user_id(new_list.user_id)
        self.validate_book_ids(new_list.book_ids)
        while db.session.query(Lists.list_id).filter_by(list_id=self.counter).scalar() is not None:
             self.counter = self.counter + 1

        new_list.list_id = self.counter
        query = Lists(list_id = new_list.list_id, list_name = new_list.list_name, user_id = new_list.user_id, book_ids = new_list.book_ids)
        db.session.add(query)
        db.session.commit()
        print(new_list.book_ids)

    def validate_user_id(self, user_id):
        if db.session.query(Users.id).filter_by(id=user_id).scalar() is None:
            api.abort(404, description="cannot find this user")

    def validate_book_ids(self, book_ids):       
        for ids in book_ids:
            if db.session.query(BookDbModel.id).filter_by(id=ids).scalar() is None:
                api.abort(404, description="cannot find one of the book ids")

    def validate_list_id(self, a_list_id):
        if db.session.query(Lists.list_id).filter_by(list_id=a_list_id).scalar() is None:
            api.abort(404, description="cannot find this list_id")

    def get_a_list(self, a_list_id):
        self.validate_list_id(a_list_id)
        a_list = Lists.query.filter_by(list_id=a_list_id).first()
        return a_list

    def update(self, a_list_id, updated_list):
        old_record = self.get_a_list(a_list_id)
        if updated_list['list_name'] is not None:
            old_record.list_name = updated_list['list_name']
        if updated_list['book_ids'] is not None:
            self.validate_book_ids(updated_list['book_ids'])
            old_record.book_ids = updated_list['book_ids']
        db.session.commit()

    def delete(self, a_list_id):
        deleted_list = self.get_a_list(a_list_id)
        db.session.delete(deleted_list)
        db.session.commit()


DAO = ListDAO()
@api.response(202, 'lists successfully obtained')
@api.response(404, 'Could not find any lists')
@api.route('/')
class ListCollection(Resource):
    def get(self):
        ''' Return a list of booklists'''
        return DAO.get_all_lists(), 202

    @api.response(202, 'list successfully created')
    @api.response(404, 'Could not create a new list')
    @api.expect(parser)
    def post(self):
        '''Creates a new list.'''
        data = parser.parse_args()
        print(data['book_ids'])
        new_list = List(0, data['list_name'], data['user_id'], data['book_ids'])
        DAO.store(new_list)
        return 'success', 202


@api.route('/<int:list_id>')
class ListOperations(Resource):
    @api.response(200, 'list successfully obtained')
    @api.response(404, 'Could not get that specific list')
    @api.marshal_with(list_model)
    def get(self, list_id):
        '''Return a certain list by id'''
        a_list = DAO.get_a_list(list_id)
        return a_list, 200

    @api.response(200, 'list successfully updated.')
    @api.response(404, 'Could not update current list')
    @api.expect(parser1)
    def put(self, list_id):
        ''' Updates a current list'''
        a_updated_list = parser1.parse_args()
        DAO.update(list_id, a_updated_list)
        return 'sucess', 200

    @api.response(200, 'list successfully deleted.')
    @api.response(404, 'list could not be deleted')
    def delete(self, list_id):
        '''Deletes a list'''
        DAO.delete(list_id)
        return 'sucess', 200
