from flask import jsonify,request,Flask,Blueprint,render_template
import bcrypt
import jwt
from datetime import datetime, timedelta

app = Flask(__name__)
memberBlueprint = Blueprint('member', __name__, url_prefix="/member")
SECRET_KEY = 'asdasdsadsad'


@memberBlueprint.route("/login", methods=['POST'])
def login_proc():
        user_id = request.form['id']
        user_pw = request.form['pw']


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
            return jsonify({'result': 'fail', 'msg': '정보 틀림'})




#cookie관리
@memberBlueprint.route("/login_check")
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
