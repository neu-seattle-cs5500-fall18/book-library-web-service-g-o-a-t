from flask_restplus import Api

from .Users import api as user_api
from .Books import api as books_api
from .BookLoans import api as loans_api


api = Api(title='G.O.A.T API', version='1.0', description='An awesome library API built by The G.O.A.Ts')

api.add_namespace(books_api)
api.add_namespace(user_api)
api.add_namespace(loans_api)

