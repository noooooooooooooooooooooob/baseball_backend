from flask import Flask
from flask import render_template
import app.api.token as token

app = Flask(__name__)

@app.route("/")
def index():

    tokenLog = token.tokenIssue()

    return render_template("/index.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
