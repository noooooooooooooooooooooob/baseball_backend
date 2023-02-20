from config import db


class User(db.Model):
    __table_args__ = {"schema": "baseball"}
    id = db.Column('id', db.Integer, primary_key=True)
    userid = db.Column(db.String(100))
    password = db.Column(db.String(100))
    team = db.Column(db.String(100))
    insertdate = db.Column(db.DateTime)
    logindate = db.Column(db.DateTime)
    updatedate = db.Column(db.DateTime)

    def __init__(self, userid, password, team, insertdate):
        self.userid = userid
        self.password = password
        self.team = team
        self.insertdate = insertdate



class Baseball(db.Model):
    __table_args__ = {"schema": "baseball"}
    id = db.Column('id', db.Integer, primary_key=True)
    userIdx = db.Column(db.Integer())
    stadium = db.Column(db.String(100))
    homeResult = db.Column(db.String(100))
    awayResult = db.Column(db.String(100))
    homeScore = db.Column(db.String(100))
    awayScore = db.Column(db.String(100))
    homeTeam = db.Column(db.String(100))
    awayTeam = db.Column(db.String(100))
    homeSP = db.Column(db.String(100))
    homeLineup = db.Column(db.JSON)
    awaySP = db.Column(db.String(100))
    awayLineup = db.Column(db.JSON)
    comment = db.Column(db.String())
    matchDate = db.Column(db.DateTime)
    insertDate = db.Column(db.DateTime)
    updateDate = db.Column(db.DateTime)

    def __init__(self, userIdx, stadium, homeResult, awayResult, homeScore, awayScore, homeTeam, awayTeam, homeLineup, awayLineup, homeSP, awaySP, comment, matchDate, insertDate, updateDate):
        self.userIdx = userIdx
        self.stadium = stadium
        self.homeResult = homeResult
        self.awayResult = awayResult
        self.homeScore = homeScore
        self.awayScore = awayScore
        self.homeTeam = homeTeam
        self.awayTeam = awayTeam
        self.homeLineup = homeLineup
        self.awayLineup = awayLineup
        self.homeSP = homeSP
        self.awaySP = awaySP
        self.comment = comment
        self.matchDate = matchDate
        self.insertDate = insertDate
        self.updateDate = updateDate

