from flask import Flask
from flask_restplus import Api

api = Api(
    title = 'G.O.A.T  API',
    version = '1.0',
    description = 'A book API powered by Flask RestPlus'
)
app = Flask(__name__)


#@app.route('/')
#def hello_world():
#    return 'We are Team Goat'
if __name__ == '__main__':
    app.run(debug = True)  #starting a development server
