from flask import Flask,request,render_template,jsonify
from app.api import member
bp = Flask(__name__)
bp.register_blueprint(member.memberBlueprint)
@bp.route("/")
def index():

    return render_template("/index.html")




if __name__ == '__main__':
    bp.run(host='0.0.0.0', port=5000, debug=True)

