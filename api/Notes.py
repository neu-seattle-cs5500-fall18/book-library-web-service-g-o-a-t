from flask_restplus import fields, Namespace, Resource, reqparse
from .SharedModel import db

api = Namespace('Notes', description='Operations related to specific users notes')

#Python notes class
class Notes:
    def __init__(self,book_id, user_id,notes_id, notes):
        self.book_id = book_id
        self.user_id = user_id
        self.notes_id = notes_id
        self.notes = notes


#Notes API
notes_api_model = api.model("Notes", {
    'book_id': fields.Integer(description='Book ID'),
    'user_id': fields.Integer(description='User ID'),
    'notes_id': fields.Integer(description='Notes ID'),
    'notes': fields.String(description='notes from the user regarding the book'),
})

#Database model for notes
class NotesDbModel (db.Model):
    book_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    notes_id = db.Column(db.Integer, primary_key=True)
    notes = db.Column(db.String(100))


#Notes DAO
class NotesDAO(object):
    def __init__(self):
        self.counter = 0

    def to_dic(self, sql_object):
        my_list = []
        for notes in sql_object:
            my_list.append({"book_id": notes.book_id, "user_id": notes.book_id,"notes_id": notes.notes_id, "notes": notes.notes})
        return my_list

    def get_all_notes(self):
        all_notes = NotesDbModel.query.all()
        return self.to_dic(all_notes)

    def store(self, new_note):
        while db.session.query(NotesDbModel.id).filter_by(id=self.counter).scalar() is not None:
            self.counter = self.counter + 1

        new_note.id = self.counter
        query = NotesDbModel(book_id= new_note.book_id, user_id=new_note.user_id, notes_id=new_note.notes_id ,notes= new_note.notes)
        db.session.add(query)
        db.session.commit()
        return new_note

    def get_a_note(self, note_id):
        a_note = NotesDbModel.query.filter_by(id=note_id).first()
        return a_note

    def update(self, note_id, updated_note):
        old_note = self.get_a_note(note_id)
        if not old_note:
            api.abort(404)
        old_note.notes = updated_note['notes']
        db.session.commit()

    def delete(self, note_id):
        deleted_note = self.get_a_note(note_id)
        if not deleted_note:
            api.abort(404)
        db.session.delete(deleted_note)
        db.session.commit()


#parser to get a note
noteparser = reqparse.RequestParser()
noteparser.add_argument('note_id', required=True)



DAO = NotesDAO()


@api.route('/')
class NoteController(Resource):
    @api.response(200, 'List of notes successfully obtained')
    @api.response(404, 'Could not get list of notes')
    def get(self):
        '''Return a list of all notes'''
        return DAO.get_all_notes(), 202


@api.route('/<int:note_id>')
class UserOperations(Resource):
    @api.response(200, 'User successfully obtained')
    @api.response(404, 'Could not get that specific user')
    @api.marshal_with(notes_api_model)
    def get(self, note_id):
        '''Return a certain user by id'''
        note = DAO.get_a_note(note_id)
        if not note:
            api.abort(404)
        else:
            return note, 200

    @api.response(200, 'User successfully updated.')
    @api.response(404, 'Could not update current user')
    @api.expect(noteparser)
    def put(self, note_id):
        ''' Updates a current user'''
        updated_note = noteparser.parse_args()
        DAO.update(note_id, updated_note)
        return 'sucess', 200

    @api.response(200, 'User successfully deleted.')
    @api.response(404, 'User could not be deleted')
    def delete(self, note_id):
        '''Deletes a user'''
        DAO.delete(note_id)
        return 'sucess', 200


