from flask import jsonify,request,Flask,Blueprint,render_template,make_response
from flask_cors import CORS
import bcrypt
import jwt
from app.api import user
import app.db as db
from datetime import datetime, timedelta

app = Flask(__name__)
userBlueprint = Blueprint('user', __name__, url_prefix="/user")
CORS(app)
SECRET_KEY = 'asdasdsadsad'

# 테스트 API
@userBlueprint.route("/test", methods=['GET'])
def test():
    return jsonify({'result': 'success', 'message': 'Hello World'})

# 회원가입 API
@userBlueprint.route("/signup", methods=['POST'])
def signUp():
    params = request.get_json()

    user_id = params['userId']
    user_pw = params['password']
    user_team = params['team']

    # data = db.User(userid = user_id, password = user_pw, team = user_team)
    # db.db.add(data)
    # db.db.commit()

    return jsonify({'result': 'success', 'message': 'Hello World'})

#토큰 발급 example
@userBlueprint.route("/signin", methods=['POST'])
def login_proc():
        params = request.get_json()

        user_id = params['userId']
        user_pw = params['password']

        # 정보가 맞는 경우
        if user_id == "test" and user_pw == "123456":
            payload = {
                'id': user_id,
                'exp': datetime.utcnow() + timedelta(seconds=60)
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

            return build_actual_response(jsonify({'result': 'success', 'token': token}))


        # 정보가 틀린 경우
        else:
            return build_actual_response(jsonify({'result': 'fail', 'msg': '정보 틀림'}))




#cookie관리
@userBlueprint.route("/login_check")
def loginCheck():
    token_receive = request.cookies.get('loginToken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        print(payload)
        return payload
    except jwt.ExpiredSignatureError:
        return "error"
    except jwt.exceptions.DecodeError:
        return "error"

def build_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response
    
def build_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response
