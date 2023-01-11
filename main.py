from flask import Flask
from datetime import datetime
from flask import render_template, request, redirect, url_for, session, jsonify
import app.api.baseball as bb
app = Flask(__name__)

@app.route("/")
def index():

    testReturn = bb.testApi()

    return render_template("/index.html", testReturn = testReturn)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
