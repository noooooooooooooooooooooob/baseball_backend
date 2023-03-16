from flask import jsonify, request, Blueprint
import jwt
import time
import app.db as db
from datetime import datetime
from config import app,SECRET_KEY, bcrypt, build_preflight_response,build_actual_response,result_make
from ..swagger import user_api, Resource, signup_model, reqparse,signin_model,signout_model
from config import fail, success
import app.swagger as sg


# 테스트 API
# @userBlueprint.route("/test", methods=['GET'])
# def test():
#     res = {'message': 'success'}
#     msg = 'success'
#     code = 200

#     return result_make(res, msg, code)

# 회원가입 API
@user_api.route("/signup")
class Signup(Resource):
    @user_api.doc('회원가입')
    @user_api.expect(signup_model)
    def post(self):

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


@user_api.route("/checkid/<string:userId>")
class checkId(Resource):
    @user_api.doc('아이디 체크')
    def get(self, userId):
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
@user_api.route("/signin")
class Signin(Resource):
    @user_api.doc('로그인')
    @user_api.expect(signin_model)
    def post(self):
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
                    'exp': int(time.time()) + 21600, # 6 hour from now
                    'user_id': idCheck.id
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
@user_api.route("/signout")
class signout(Resource):
    @user_api.doc('로그아웃')
    @user_api.expect(signout_model)
    def post(self):
        if request.method == 'OPTIONS':
            return build_preflight_response()
        
        token_receive = request.cookies.get('loginToken')
        
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        payload['exp'] = 1

        new_token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        res = {}
        msg = 'success'
        code = 200

        res["token"] = new_token

        return result_make(res, msg, code)

# cookie관리
@user_api.route("/signin-check")
class signinCheck(Resource):
    @user_api.doc('로그인확인')
    @user_api.expect(sg.signCheck_model)
    def post(self):   
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


