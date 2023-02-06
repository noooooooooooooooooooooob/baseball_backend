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


