from flask import jsonify, request, Blueprint, make_response
import jwt
import time
import app.db as db
from datetime import datetime
from config import app,build_actual_response,build_preflight_response
from ..swagger import baseball_api, Resource
import app.swagger as sg


# 직관정보등록
@baseball_api.route("/create")
class baseballCreate(Resource):
    @baseball_api.doc('직관정보등록')
    @baseball_api.expect(sg.baseball_create_model)
    def post(self):
        if request.method == 'OPTIONS':
            return build_preflight_response()
        


        return "test"
