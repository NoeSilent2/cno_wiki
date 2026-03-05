import json
from flask import Flask, render_template


app = Flask(__name__)


@app.route("/")
def read_root():
    return render_template("main.html")


with open('./data/fakemon.json', 'r', encoding='utf-8') as file:
    fakemondata = json.load(file)
@app.route("/fakemon")
def get_fakemon():
    return render_template("fakemon.html", fakemon=fakemondata)


with open('./data/moves.json', 'r', encoding='utf-8') as file:
    cmovesdata = json.load(file)
@app.route("/moves")
def get_moves():
    return render_template("moves.html", moves=cmovesdata)