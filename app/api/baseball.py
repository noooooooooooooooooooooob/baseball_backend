from flask import jsonify, request, Blueprint, make_response
import jwt
import time
import app.db as db
from datetime import datetime
from config import app,build_actual_response,build_preflight_response,result_make
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

# 직관 정보 전체 조회
@baseball_api.route("/all/<int:userIdx>")
class baseballSearchAll(Resource):
    @baseball_api.doc('직관정보전체조회')
    def get(self, userIdx):
        res = {}
        msg = 'success'
        code = 200

        if request.method == 'OPTIONS':
            return build_preflight_response()
        
        baseball_data = db.Baseball.query.filter(db.Baseball.userIdx == userIdx).all()
        user_data = db.User.query.filter_by(id = userIdx).first()

        data_list = []

        for row in baseball_data:
            data_dict = {
                "title": row.title,
                "home": row.homeTeam,
                "away": row.awayTeam,
                "homeResult": row.homeResult,
                "awayResult": row.awayResult,
                "homeScore": row.homeScore,
                "awayScore": row.awayScore,
                "matchData": row.matchDate.strftime("%Y-%m-%d %H:%M:%S %A"),
                "insertDate": row.insertDate.strftime("%Y-%m-%d %H:%M:%S %A"),
                "id": row.id
            }
            data_list.append(data_dict)

        # 승/패/승률 데이터를 계산합니다.
        win_count = 0
        lose_count = 0
        taem = user_data.team

        for row in baseball_data:
            if taem == row.homeTeam:
                if row.homeResult == "승":
                    win_count += 1
                else:
                    lose_count += 1
            
            if taem == row.awayTeam:
                if row.awayResult == "승":
                    win_count += 1
                else:
                    lose_count += 1

        total_count = win_count + lose_count
        odds = round(win_count / total_count * 100, 1)

        res = {
            "data": data_list,
            "stats": {
                "win": win_count,
                "lose": lose_count,
                "odds": odds
            }
        }
        return result_make(res, msg, code)
