from flask import Flask
from flask_restful import Api
from models import db, User
import os

app = Flask(__name__)
api = Api(app)

app.config['DEBUG'] = True
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

db.init_app(app)

@app.route('/')
def index():
    return 'Hello World'

import models, resources

api.add_resource(resources.addUserLocation, '/addLocation')
api.add_resource(resources.getUserLocation, '/getLocation')

if __name__ == "__main__":
    app.run()
