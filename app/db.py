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
    home = db.Column(db.String(100))
    matchResult = db.Column(db.String(100))
    matchTeam = db.Column(db.String(100))
    homeSP = db.Column(db.String(100))
    homeLineUp = db.Column(db.JSON)
    awaySP = db.Column(db.String(100))
    awayLineUp = db.Column(db.JSON)
    comment = db.Column(db.String())
    matchDate = db.Column(db.DateTime)
    insertDate = db.Column(db.DateTime)
    updateDate = db.Column(db.DateTime)

    def __init__(self, home, matchResult, homeSP, homeLineUp, awaySP, awayLineUp, comment, matchDate, insertDate, updateDate):
        self.home = home
        self.matchResult = matchResult
        self.homeSP = homeSP
        self.homeLineUp = homeLineUp
        self.awaySP = awaySP
        self.awayLineUp = awayLineUp
        self.comment = comment
        self.matchDate = matchDate
        self.insertDate = insertDate
        self.updateDate = updateDate

