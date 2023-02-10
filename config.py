from flask import Flask
from flask_restx import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://qpdqfreb:vupguJOZHn0GifZiWvj7Z6kNk_acbE7t@chunee.db.elephantsql.com/qpdqfreb"
app.config['SECRET_KEY'] = "12346erwef"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
SECRET_KEY = "asd12342r23f"
db = SQLAlchemy(app)
