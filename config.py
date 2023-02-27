from flask import Flask,make_response,jsonify
from flask_restx import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://qpdqfreb:vupguJOZHn0GifZiWvj7Z6kNk_acbE7t@chunee.db.elephantsql.com/qpdqfreb"
app.config['SECRET_KEY'] = "12346erwef"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
SECRET_KEY = "asd12342r23f"
db = SQLAlchemy(app)

fail = '요청 값을 다시 한 번 확인해주세요.'
success = 'success'

def build_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

def build_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

def result_make(res, msg, code):
    result = {'result': res, 'message': msg}

    return make_response(jsonify(result), code)

def date_to_string(date):
    return date.strftime("%Y-%m-%d %H:%M:%S")