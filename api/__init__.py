from flask_restplus import Api
from flask import Flask
from .Users import api as usermodel_api
from .Books import api as books_api
from .BookLoans import api as loans_api
from .BookList import api as list_api
# from .Notes import api as notes_api

api = Api(title='G.O.A.T API', version='1.0', description='An awesome library API built by The G.O.A.Ts')

api.add_namespace(books_api)
api.add_namespace(usermodel_api)
api.add_namespace(loans_api)
api.add_namespace(list_api)
# api.add_namespace(notes_api)



