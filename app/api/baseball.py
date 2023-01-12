from flask import Blueprint, request, make_response, jsonify, send_file, session, render_template, redirect
from bs4 import BeautifulSoup
app = Blueprint('api', __name__)

@app.route("/test")
def testApi():

    team = "LG"
    date = "04.01"





    return "Hello World"
