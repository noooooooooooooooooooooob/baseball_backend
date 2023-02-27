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
    userIdx = db.Column(db.Integer)
    title = db.Column(db.String)
    stadium = db.Column(db.String)
    homeResult = db.Column(db.String)
    awayResult = db.Column(db.String)
    homeScore = db.Column(db.Integer)
    awayScore = db.Column(db.Integer)
    homeTeam = db.Column(db.String)
    awayTeam = db.Column(db.String)
    homeLineup = db.Column(db.ARRAY(db.String))
    homeSP = db.Column(db.String)
    awayLineup = db.Column(db.ARRAY(db.String))
    awaySP = db.Column(db.String)
    comment = db.Column(db.Text)
    matchDate = db.Column(db.DateTime(timezone = True), nullable = False)
    insertDate = db.Column(db.DateTime(timezone = True), nullable = False)
    updateDate = db.Column(db.DateTime(timezone = True), nullable = False)

    def __init__(self, userIdx, title, stadium, homeResult, awayResult, homeScore, awayScore, homeTeam, awayTeam, homeLineup, awayLineup, homeSP, awaySP, comment, matchDate):
        self.userIdx = userIdx
        self.title = title
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

