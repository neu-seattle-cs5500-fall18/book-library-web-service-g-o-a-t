from flask_restplus import Api

from .Users import ns as user_ns
from .Books import ns as books_ns


api = Api(title='G.O.A.T API', version='1.0', description='A simple library API for course CS5500')

api.add_namespace(books_ns)
api.add_namespace(user_ns)

