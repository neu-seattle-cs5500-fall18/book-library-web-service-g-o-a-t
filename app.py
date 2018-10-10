from flask import Flask
from flask_restplus import Api, Resource


app = Flask(__name__)
api = Api(app)


app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
