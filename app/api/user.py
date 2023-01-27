from flask import jsonify, request, Flask, Blueprint, render_template, make_response, abort
from flask_bcrypt import Bcrypt
import jwt
from app.api import user
import app.db as db
from datetime import datetime, timedelta
from http import HTTPStatus

app = Flask(__name__)
userBlueprint = Blueprint('user', __name__, url_prefix="/user")
app.register_blueprint(userBlueprint)
SECRET_KEY = 'asdasdsadsad'
BCRYPT_LEVEL = 10
bcrypt = Bcrypt(app)


# 테스트 API
@userBlueprint.route("/test", methods=['GET'])
def test():
    return jsonify({'result': 'success', 'message': 'Hello World'})


# 회원가입 API
@userBlueprint.route("/signup", methods=['POST'])
def signUp():
    params = request.get_json()
    userPassword = bcrypt.generate_password_hash(params['password']).decode()
    if request.method == 'OPTIONS':
        return build_preflight_response()

    if len(params) == 3:
        userSignup = db.User(userid=params['userId'], password=userPassword, team=params['team'],
                             insertdate=datetime.now())
        db.db.session.add(userSignup)
        db.db.session.commit()
        return make_response('success', 201)
    else:

        return make_response('요청 값을 다시 한 번 확인해주세요.', 400)


@userBlueprint.route("/checkId", methods=['GET'])
def checkId():
    userId = request.args.get("userId")

    if userId is not None:

        idCheck = db.User.query.filter( db.User.userid == userId).all()
        print(len(idCheck))
        if len(idCheck) == 0:
            return make_response('사용 가능한 아이디 입니다.', 200)
        else:
            return make_response('이미 존재하는 아이디 입니다.', 200)
    else:
        return make_response("요청 값을 다시 한 번 확인해주세요.", 400)

# 토큰 발급 example
@userBlueprint.route("/signin", methods=['OPTIONS', 'POST'])
def login_proc():
    if request.method == 'OPTIONS':
        return build_preflight_response()

    params = request.get_json()




    if len(params) == 2:
        # 정보가 맞는 경우
        user_id = params['userId']
        user_pw = params['password']
        idCheck = db.User.query.filter_by(userid = user_id).first()

        if idCheck and bcrypt.check_password_hash(idCheck.password, user_pw):
            payload = {
                'id': user_id,
                'exp': datetime.utcnow() + timedelta(seconds=60)
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

            return make_response(token, 200)
        else:

            if idCheck:
                return make_response('아이디 혹은 비밀번호를 다시 한 번 확인해주세요.', 400)
            else:
                return make_response('존재하지 않는 아이디 입니다.', 400)
    else:
        return make_response('요청 값이 잘못 되었습니다.', 400)
# cookie관리
@userBlueprint.route("/login_check")
def loginCheck():
    token_receive = request.cookies.get('loginToken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return "error"
    except jwt.exceptions.DecodeError:
        return "error"


@userBlueprint.route("/findId")
def findId():
    userName = request.args.get("name")
    userPhone = request.args.get("phone")

    idCheck = db.User.query.filter(name=userName, phone=userPhone)

    return jsonify({'result': 'success'})


def build_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response


def build_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response
