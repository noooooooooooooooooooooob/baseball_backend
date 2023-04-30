from flask import Flask,make_response,jsonify,request
from flask_restx import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from functools import wraps
import jwt
import app.db as db2
from dotenv import load_dotenv
import os 

load_dotenv()
app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URL')
app.config['SECRET_KEY'] = "12346erwef"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
SECRET_KEY = "asd12342r23f"
db = SQLAlchemy(app)

fail = '요청 값을 다시 한 번 확인해주세요.'
success = 'success'
naver_api_url = os.environ.get("NAVER_API_URL")

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

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        res = {}
        msg = '로그인후 이용 가능합니다'
        code = 401



        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            token = auth_header.split(" ")[1]
        if not token:

            return result_make(res, msg, code)
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            user_id = payload['user_id']
            user = db2.User.query.filter_by(id=user_id).first()
            kwargs['user'] = user
        except:
            return result_make(res,msg,code)
        return f(*args, **kwargs)
    return decorated