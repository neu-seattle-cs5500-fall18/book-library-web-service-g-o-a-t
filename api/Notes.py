from flask_restplus import fields, Namespace, Resource, reqparse
from .SharedModel import db

api = Namespace('Notes', description='Operations related to specific users notes')

#Python notes class
class Notes(object):
    def __init__(self, id, book_id, user_id, notes):
        self.id = id
        self.book_id = book_id
        self.user_id = user_id
        self.notes = notes


#Notes API
notes_api_model = api.model("Notes", {
    'id': fields.Integer(description='Notes ID'),
    'book_id': fields.Integer(description='Book ID'),
    'user_id': fields.Integer(description='User ID'),
    'notes': fields.String(description='notes from the user regarding the book'),
})

#Database model for notes
class NotesDbModel (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    notes = db.Column(db.String(100))


#Notes DAO
class NotesDAO(object):
    def __init__(self):
        self.counter = 0

    def to_dic(self, sql_object):
        my_list = []
        for notes in sql_object:
            my_list.append({"id": notes.id, "book_id": notes.book_id, "user_id": notes.user_id, "notes": notes.notes})
        return my_list

    def get_all_notes(self):
        all_notes = NotesDbModel.query.all()
        return self.to_dic(all_notes)

    def get_notes_by_user(self, user_id):
        all_notes = NotesDbModel.query.filter_by(user_id=user_id)
        return self.to_dic(all_notes)

    def get_notes_by_book(self, book_id):
        all_notes = NotesDbModel.query.filter_by(book_id=book_id)
        return self.to_dic(all_notes)

    def get_notes_only(self, book_id):
        note = NotesDbModel.query.with_entities(NotesDbModel.user_id, NotesDbModel.notes).filter_by(book_id=book_id).all()
        return note
    def store(self, new_note):
        while db.session.query(NotesDbModel.id).filter_by(id=self.counter).scalar() is not None:
            self.counter = self.counter + 1

        new_note.id = self.counter
        query = NotesDbModel(id=new_note.id, book_id=new_note.book_id, user_id=new_note.user_id, notes=new_note.notes)
        db.session.add(query)
        db.session.commit()
        return new_note

    def get_a_note(self, note_id):
        a_note = NotesDbModel.query.filter_by(id=note_id).first()
        return a_note

    def update(self, note_id, updated_note):
        old_note = self.get_a_note(note_id)
        print(old_note.id)
        if not old_note:
            api.abort(404)
        if updated_note['book_id'] is not None:
            old_note.book_id = updated_note['book_id']
        print(updated_note['user_id'])
        if updated_note['user_id'] is not None:
            old_note.user_id = updated_note['user_id']
        if updated_note['notes'] is not None:
            old_note.notes = updated_note['notes']
        print(updated_note['user_id'])
        db.session.commit()

    def delete(self, note_id):
        deleted_note = self.get_a_note(note_id)
        if not deleted_note:
            api.abort(404)
        db.session.delete(deleted_note)
        db.session.commit()

    def delete_by_user(self, user_id, note_id):
        deleted_note = self.get_a_note(note_id)
        if not deleted_note:
            api.abort(404, description= "that note id doesn't exist")
        if deleted_note.user_id == user_id:
            db.session.delete(deleted_note)
            db.session.commit(0)
        else:
            api.abort(404, description= "could not delete a note from that specific user")



#parser to get a note
noteparser = reqparse.RequestParser()
noteparser.add_argument('book_id', type=int)
noteparser.add_argument('user_id', type=int)
noteparser.add_argument('notes', type=str)



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
    @api.response(200, 'note successfully obtained')
    @api.response(404, 'Could not get that specific note')
    @api.marshal_with(notes_api_model)
    def get(self, note_id):
        '''Return a certain note by id'''
        note = DAO.get_a_note(note_id)
        if not note:
            api.abort(404)
        else:
            return note, 200

    @api.response(200, 'note successfully updated.')
    @api.response(404, 'Could not update current note')
    @api.expect(noteparser)
    def put(self, note_id):
        ''' Updates a current note'''
        updated_note = noteparser.parse_args()
        DAO.update(note_id, updated_note)
        return 'sucess', 200

    @api.response(200, 'note successfully deleted.')
    @api.response(404, 'note could not be deleted')
    def delete(self, note_id):
        '''Deletes a note'''
        DAO.delete(note_id)
        return 'sucess', 200
