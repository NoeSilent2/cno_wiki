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

with open('./data/species.json', 'r', encoding='utf-8') as file:
    speciesdata = json.load(file)
@app.route("/species")
def get_species():
    return render_template("species.html", species=speciesdata)

speciesdict = {}
for i, species in enumerate(speciesdata):
    speciesdict[species['internal_name']] = i
@app.route("/species/<name>")
def get_species_specific(name):
    name = name.lower()
    if name in speciesdict:
        species = speciesdata[speciesdict[name]]
        return render_template("species_specific.html", species=species)
    else:
        return redirect(url_for('get_species'))



with open('./data/cmoves.json', 'r', encoding='utf-8') as file:
    cmovesdata = json.load(file)
@app.route("/cmoves")
def get_cmoves():
    return render_template("cmoves.html", moves=cmovesdata)

with open('./data/moves.json', 'r', encoding='utf-8') as file:
    movesdata = json.load(file)
@app.route("/moves")
def get_moves():
    return render_template("moves.html", moves=movesdata)