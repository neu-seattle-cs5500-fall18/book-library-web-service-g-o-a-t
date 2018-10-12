
from flask import Flask
from flask_restplus import Api, Resource
from Operations import app
#app = Flask(__name__)
#api = Api(app)

#@app.route('/')
#def hello_world():
#    return 'We are Team Goat'
if __name__ == '__main__':
    app.run(debug = True)
