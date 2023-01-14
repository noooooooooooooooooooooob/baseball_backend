from flask import Flask,request,render_template,jsonify
from app.api import member
import app.db as db
app = Flask(__name__)



app.register_blueprint(member.memberBlueprint)

@app.route("/")
def index():

    print(db.User.query.all())

    return render_template("/index.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

