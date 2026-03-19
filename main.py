import json
import random
import hashlib
from datetime import date
from flask import Flask, render_template, redirect, url_for


app = Flask(__name__)


with open('./data/species.json', 'r', encoding='utf-8') as file:
    speciesdict = json.load(file)

def get_daily_object():
    today = date.today()
    random.seed(int(hashlib.md5(f"{today.year}{today.month}{today.day}".encode()).hexdigest()[:8], 16))
    species_id = random.choice(list(speciesdict.keys()))
    rspecies = random.choice(speciesdict[species_id])
    isShiny = 'normal'
    if random.randint(1, 50) == 1:
        isShiny = 'shiny'
    return {
        'name': rspecies.get('name', 'ERROR'),
        'img': rspecies.get('alt_internal_name', 'unown-qm'),
        'link': species_id,
        'shiny': isShiny
    }





@app.route("/")
def read_root():
    return render_template("main.html", pokemon=get_daily_object())


with open('./data/fakemon_simple.json', 'r', encoding='utf-8') as file:
    fakemontable = json.load(file)
@app.route("/fakemon")
def get_fakemon():
    return render_template("fakemon.html", fakemon=fakemontable)

with open('./data/species_simple.json', 'r', encoding='utf-8') as file:
    speciestable = json.load(file)
@app.route("/species")
def get_species():
    return render_template("species.html", species=speciestable)



@app.route("/species/<name>")
def get_species_specific(name):
    name = name.lower()
    if name == "random":
        random.seed()
        species = random.choice(list(speciesdict.keys()))
        if species:
            return redirect(url_for('get_species_specific', name=species))
    elif name in speciesdict:
        species = speciesdict[name]
        return render_template("species_specific.html", species_forms=species)
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



@app.route("/staff")
def get_staff():
    return render_template("staff.html")