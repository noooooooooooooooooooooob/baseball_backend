from flask_restx import Api, Resource, fields, reqparse
from config import app


api = Api(app, version='1.0', title='API 문서', description='Swagger 문서', doc="/api-docs")

user_api = api.namespace('user', description='유저 API')


signup_model = api.model('Signup', {
    'userId': fields.String(required=True, description='사용자 ID'),
    'password': fields.String(required=True, description='비밀번호'),
    'team': fields.String(required=True, description='팀명'),
})

signin_model = api.model('Signin', {
    'userId': fields.String(required=True, description='사용자 ID'),
    'password': fields.String(required=True, description='비밀번호'),
})

signout_model = api.model('Signout', {
    'token': fields.String(required=True, description='토큰')
})

signCheck_mode = api.model('SignCheck', {
        'token': fields.String(required=True, description='토큰')
})