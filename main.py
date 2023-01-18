from flask import Flask,request,render_template,jsonify,make_response
from app.api import user
import app.db as db
app = Flask(__name__)

app.register_blueprint(user.userBlueprint)

@app.route("/")
def index():


    return render_template("/index.html", test = db.User.query.all())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)

