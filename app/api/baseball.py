from flask import Blueprint, request, make_response, jsonify, send_file, session, render_template, redirect

app = Blueprint('api', __name__)

@app.route("/test")
def testApi():


    return "Hello World"
