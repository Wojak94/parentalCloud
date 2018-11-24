from flask import Flask
from models import db
import os

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

db.init_app(app)

@app.route('/')
def index():
    return 'Hello World'

if __name__ == "__main__":
    app.run()