from flask import Flask,request,render_template,jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://qpdqfreb:vupguJOZHn0GifZiWvj7Z6kNk_acbE7t@chunee.db.elephantsql.com/qpdqfreb"
app.config['SECRET_KEY'] = "12346erwef"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    __table_args__ = {"schema": "baseball"}
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    email = db.Column(db.String(100))
    userid = db.Column(db.String(100))
    password = db.Column(db.String(100))
    team = db.Column(db.String(100))
    insertdate = db.Column(db.DateTime)
    logindate = db.Column(db.DateTime)
    updatedate = db.Column(db.DateTime)

    def __init__(self, name, phone, email, userId, password, team):
        self.name = name
        self.phone = phone
        self.email = email
        self.userId = userId
        self.password = password
        self.team = team


