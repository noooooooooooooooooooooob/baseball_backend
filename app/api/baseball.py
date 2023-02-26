from flask import jsonify, request, Blueprint, make_response
import jwt
import time
import app.db as db
from datetime import datetime
from config import app,build_actual_response,build_preflight_response,result_make
from ..swagger import baseball_api, Resource
import app.swagger as sg
import requests
import json

# 직관정보등록
@baseball_api.route("/create")
class baseballCreate(Resource):
    @baseball_api.doc('직관정보등록')
    @baseball_api.expect(sg.baseball_create_model)
    def post(self):
        if request.method == 'OPTIONS':
            return build_preflight_response()
        params = request.get_json()

        url = params['matchDate'].replace("-","") + TeamCode(params['away']) + TeamCode(params['home'])+ "0" + params['matchDate'][:4]
        now = datetime.now()
        print(url)
        formatted_date = now.strftime("%Y-%m-%d")
        baseball_res = requests.get('https://api-gw.sports.naver.com/schedule/games/' + url + '/preview')



        if baseball_res.status_code == 200:
            awayLineup = baseball_res.json()['result']['previewData']['awayTeamLineUp']['fullLineUp']
            homeLineup = baseball_res.json()['result']['previewData']['homeTeamLineUp']['fullLineUp']
            gameData = requests.get("https://api-gw.sports.naver.com/schedule/games/" + url)

            homeHitter = []
            awayHitter = []

            for h in homeLineup:
                if h['positionName'] != "선발투수":
                    hitter = h['positionName'] + ' ' + h['playerName']
                    homeHitter.append(hitter)

            for a in awayLineup:
                if a['positionName'] != "선발투수":
                    hitter = a['positionName'] + ' ' + a['playerName']
                    awayHitter.append(hitter)        
            


            BaseballData = db.Baseball(
                userIdx="1", 
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
                matchDate= params['matchDate'],
                insertDate=formatted_date,
                updateDate=formatted_date
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
            data_dict = {
                "title": row.title,
                "home": {
                    "team": row.homeTeam,
                    "result": row.homeResult,
                    "score": row.homeScore,
                },
                "away": {
                    "team": row.awayTeam,
                    "result": row.awayResult,
                    "score": row.awayScore,
                },
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