from flask import jsonify, request, Blueprint, make_response
import jwt
import time
import app.db as db
from datetime import datetime
from config import app,SECRET_KEY, bcrypt

userBlueprint = Blueprint('user', __name__, url_prefix="/user")
app.register_blueprint(userBlueprint)

fail = '요청 값을 다시 한 번 확인해주세요.'
success = 'success'

# 테스트 API
@userBlueprint.route("/test", methods=['GET'])
def test():
    res = {'message': 'success'}
    msg = 'success'
    code = 200

    return result_make(res, msg, code)

# 회원가입 API
@userBlueprint.route("/signup", methods=['OPTIONS', 'POST'])
def signUp():
    if request.method == 'OPTIONS':
        return build_preflight_response()

    res = {}
    msg = 'success'
    code = 201

    params = request.get_json()
    userPassword = bcrypt.generate_password_hash(params['password']).decode()

    if len(params) == 3:
        userSignup = db.User(userid=params['userId'], password=userPassword, team=params['team'],
                             insertdate=datetime.now())
        db.db.session.add(userSignup)
        db.db.session.commit()
        
    else:
        code = 400
        msg = fail

    return result_make(res, msg, code)

@userBlueprint.route("/checkid", methods=['OPTIONS', 'GET'])
def checkId():
    if request.method == 'OPTIONS':
        return build_preflight_response()
    
    userId = request.args.get("userId")
    
    res = {}
    msg = 'success'
    code = 200

    if userId is not None:
        idCheck = db.User.query.filter( db.User.userid == userId).all()

        if len(idCheck) == 0:
            msg = '사용 가능한 아이디 입니다.'
        else:
            msg = '이미 존재하는 아이디 입니다.'
    else:
        code = 400 
        msg = fail
    
    return result_make(res, msg, code)

# 토큰 발급 example
@userBlueprint.route("/signin", methods=['OPTIONS', 'POST'])
def signin():
    if request.method == 'OPTIONS':
        return build_preflight_response()
    
    res = {}
    msg = 'success'
    code = 200
    
    params = request.get_json()

    if len(params) == 2:
        # 정보가 맞는 경우
        user_id = params['userId']
        user_pw = params['password']
        idCheck = db.User.query.filter_by(userid = user_id).first()

        if idCheck and bcrypt.check_password_hash(idCheck.password, user_pw):
            payload = {
                'id': user_id,
                'iat': int(time.time()),
                'exp': int(time.time()) + 21600 # 6 hour from now
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
            res["token"] = token
        else:
            msg = "아이디 혹은 비밀번호를 다시 한 번 확인해주세요."
    else:
        code = 400
        msg = fail
    
    return result_make(res, msg, code)

# 로그아웃
@userBlueprint.route("/signout", methods=['OPTIONS', 'POST'])
def signin():
    res = {}
    msg = 'success'
    code = 200

    return result_make(res, msg, code)

# cookie관리
@userBlueprint.route("/signin-check", methods=['OPTIONS', 'GET'])
def signinCheck():
    if request.method == 'OPTIONS':
        return build_preflight_response()

    token_receive = request.cookies.get('loginToken')
    
    res = {}
    msg = 'success'
    code = 200
    
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        res = dict(payload)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        msg = '유효하지 않은 토큰 정보 입니다.'
        code = 403

    return result_make(res, msg, code)

# 고인
# @userBlueprint.route("/findId")
# def findId():
#     userName = request.args.get("name")
#     userPhone = request.args.get("phone")

#     idCheck = db.User.query.filter(name=userName, phone=userPhone)

#     return result_make(res, msg, code)

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
