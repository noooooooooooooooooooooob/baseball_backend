from flask import jsonify, request, Blueprint, make_response
import jwt
import time
import app.db as db
from datetime import datetime
from config import app,build_actual_response,build_preflight_response,result_make, token_required, date_to_string
from ..swagger import baseball_api, Resource
import app.swagger as sg
import requests
import json

# 직관정보등록
@baseball_api.route("/create")
class baseballCreate(Resource):
    @token_required
    @baseball_api.doc('직관정보등록')
    @baseball_api.expect(sg.baseball_create_model)
    def post(self):
        if request.method == 'OPTIONS':
            return build_preflight_response()
        params = request.get_json()
        url = params['matchDate'].replace("-","") + TeamCode(params['away']) + TeamCode(params['home'])+ "0" + params['matchDate'][:4]
        baseball_res = requests.get('https://api-gw.sports.naver.com/schedule/games/' + url + '/preview')
        if baseball_res.status_code == 200:
            awayLineup = baseball_res.json()['result']['previewData']['awayTeamLineUp']['fullLineUp']
            homeLineup = baseball_res.json()['result']['previewData']['homeTeamLineUp']['fullLineUp']
            gameData = requests.get("https://api-gw.sports.naver.com/schedule/games/" + url)
            homeHitter = []
            awayHitter = []
            if gameData.json()['result']['game']['statusCode'] != "RESULT":
                res = {}
                msg = '해당 날짜에 경기 정보가 없습니다'
                code = 400
                return result_make(res, msg, code)


            for h in homeLineup:
                if h['positionName'] != "선발투수":
                    hitter = h['positionName'] + ' ' + h['playerName']
                    homeHitter.append(hitter)

            for a in awayLineup:
                if a['positionName'] != "선발투수":
                    hitter = a['positionName'] + ' ' + a['playerName']
                    awayHitter.append(hitter)



            BaseballData = db.Baseball(
                userIdx= params['userIdx'], 
                title=params['matchDate'] + params['away'] + " VS " + params['home'],
                stadium=gameData.json()['result']['game']['stadium'],
                homeResult= "승" if gameData.json()['result']['game']['winner'] == "HOME" else "패",
                awayResult= "승" if gameData.json()['result']['game']['winner'] == "AWAY" else "패",
                homeScore= gameData.json()['result']['game']['homeTeamScore'],
                awayScore= gameData.json()['result']['game']['awayTeamScore'],
                homeTeam= gameData.json()['result']['game']['homeTeamName'],
                awayTeam= gameData.json()['result']['game']['awayTeamName'],
                homeSP = homeLineup[0]['playerName'],
                homeLineup= homeHitter,
                awaySP= awayLineup[0]['playerName'],
                awayLineup= awayHitter,
                comment= params['comment'],
                matchDate= gameData.json()['result']['game']['gameDateTime']
            )
            db.db.session.add(BaseballData)
            db.db.session.commit()
            res = {}
            msg = 'success'
            code = 201
        elif baseball_res.status_code == 404:
            res = {}        
            msg = '해당 날짜에 경기 정보가 없습니다'
            code = 400
        return result_make(res, msg, code)

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
            data_dict['title'] = row.title
            data_dict['stadium'] = row.stadium
            data_dict['home'] = {
                "team": row.homeTeam,
                "result": row.homeResult,
                "score": row.homeScore
            }
            data_dict['away'] = {
                "team": row.awayTeam,
                "result": row.awayResult,
                "score": row.awayScore
            }
            data_dict['matchData'] = date_to_string(row.matchData)
            data_dict['insertDate'] = date_to_string(row.insertDate)
            data_dict['id'] = row.id
            
            data_list.append(data_dict)

        # 승/패/승률 데이터를 계산합니다.
        win_count = 0
        lose_count = 0
        team = user_data.team

        for row in baseball_data:
            if team == row.homeTeam:
                if row.homeResult == "승":
                    win_count += 1
                else:
                    lose_count += 1
            
            if team == row.awayTeam:
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

# 직관 상세 정보 조회
@baseball_api.route("/detail/<int:baseballId>")
class baseballSearchAll(Resource):
    @baseball_api.doc('직관정보전체조회')
    def get(self, baseballId):
        res = {}
        msg = 'success'
        code = 200

        if request.method == 'OPTIONS':
            return build_preflight_response()
        data = db.Baseball.query.filter_by(id = baseballId).first()
        
        res['title'] = data.title
        res['staium'] = data.stadium
        res['home'] = {
            "team": data.homeTeam,
            "result": data.homeResult,
            "score": data.homeScore,
            "sp": data.homeSP,
            "lineUp": data.homeLineup
        }
        res['away'] = {
            "team": data.awayTeam,
            "result": data.awayResult,
            "score": data.awayScore,
            "sp": data.awaySP,
            "lineUp": data.awayLineup
        }
        res['comment'] = data.comment
        res['matchData'] = date_to_string(data.matchDate)
        res['insertDate'] = date_to_string(data.insertDate)
        if hasattr(data, "updateDate"):
            res['updateDate']: date_to_string(data.updateDate)
        res['id']: data.id

        return result_make(res, msg, code)


def TeamCode(team):
    if team == "LG 트윈스":
        team = "LG"
    elif team == "키움 히어로즈":
        team = "WO"
    elif team == "두산 베어스":
        team = "OB"
    elif team == "한화 이글스":
        team = "HH"
    elif team == "NC 다이노스":
        team = "NC"
    elif team == "KT 위즈":
        team = "KT"
    elif team == "KIA 타이거즈":
        team = "HT"
    elif team == "롯데 자이언츠":
        team = "LT"
    elif team == "삼성 라이온즈":
        team = "SS"
    elif team == "SSG 랜더스":
        team = "SK"
    return team