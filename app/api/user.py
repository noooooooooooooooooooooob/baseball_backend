from flask import jsonify,request,Flask,Blueprint,render_template,make_response
from flask_bcrypt import Bcrypt
import jwt
from app.api import user
import app.db as db
from datetime import datetime, timedelta

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
    userPassword = bcrypt.generate_password_hash(params['password'])
    if request.method == 'OPTIONS':
        return build_preflight_response()

    userSignup = db.User(name=params['name'], phone=params['phone'], email=params['email'], userid = params['userId'], password=userPassword, team=params['team'], insertdate = datetime.now())

    #insert 테스트
    #userSignup = db.User(name='테스트 이름', phone='010-1234-1234', email='noob@gmail.com', userid='testid_1234',
    #                    password=bcrypt.generate_password_hash('testpw'), team='LG', insertdate=datetime.now())

    db.db.session.add(userSignup)
    db.db.session.commit()
    return jsonify({'result': 'success', 'message': 'Hello World'})

@userBlueprint.route("/checkId", methods=['GET'])
def checkId():

    userId = request.args.get("userId")

    idCheck = db.User.query.filter_by(id='{}'.format(userId))

    if idCheck is None:
        return jsonify({'result': 'success', 'message': 'id have no'})
    else:
        return jsonify({'result': 'fail', 'message': 'id is already'})
#토큰 발급 example
@userBlueprint.route("/signin", methods=['OPTIONS', 'POST'])
def login_proc():
    if request.method == 'OPTIONS':
        return build_preflight_response()

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

        return jsonify({'result': 'success', 'token': token})

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
