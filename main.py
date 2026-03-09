import json
from flask import Flask, render_template, redirect, url_for


app = Flask(__name__)


@app.route("/")
def read_root():
    return render_template("main.html")


with open('./data/fakemon.json', 'r', encoding='utf-8') as file:
    fakemondata = json.load(file)
@app.route("/fakemon")
def get_fakemon():
    return render_template("fakemon.html", fakemon=fakemondata)

@app.route("/species")
def species_redirect():
    return redirect(url_for('get_fakemon'))

fakemondict = {}
for fakemon in fakemondata:
    fakemondict[fakemon['internal_name']] = fakemon
@app.route("/species/<name>")
def get_fakemon_specific(name):
    name = name.lower()
    if name in fakemondict:
        fakemon = fakemondict[name]
        return render_template("species_specific.html", species=fakemon)
    else:
        return redirect(url_for('get_fakemon'))

with open('./data/moves.json', 'r', encoding='utf-8') as file:
    cmovesdata = json.load(file)
@app.route("/moves")
def get_moves():
    return render_template("moves.html", moves=cmovesdata)