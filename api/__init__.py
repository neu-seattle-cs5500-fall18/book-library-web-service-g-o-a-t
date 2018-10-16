from flask_restplus import Api

from .Users import ns as user_ns
from .Books import ns as books_ns


api = Api(title='G.O.A.T API', version='1.0', description='An awesome library API built by The G.O.A.Ts')

api.add_namespace(books_ns)
api.add_namespace(user_ns)

