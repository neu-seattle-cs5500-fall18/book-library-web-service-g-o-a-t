from flask import Flask
from flask_restplus import Api
from Book import app

app = Flask(__name__)

api = Api(app, version='1.0', title='G.OA.T API',
          description='A book API powered by Flask Restplus',
          )

if __name__ == '__main__':
    app.run(debug=True)  # starting a development server
