from flask import jsonify
import bcrypt
import jwt
from datetime import datetime, timedelta

SECRET_KEY = 'asdasdsadsad'
def tokenIssue():

    id ="testId"
    pw = "12345678"

    if ("testId" == id and
            "12345678" == pw):
        payload = {
            'id': id,
            'exp': datetime.utcnow() + timedelta(seconds=60)  # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'result': 'success', 'token': token})
    else:
        return jsonify({'result': 'fail'})
