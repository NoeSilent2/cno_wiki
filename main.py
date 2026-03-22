import json
import random
import hashlib
from datetime import date
from flask import Flask, render_template, redirect, url_for, send_from_directory


app = Flask(__name__)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico', max_age=31536000)


with open('./data/species.json', 'r', encoding='utf-8') as file:
    speciesdict = json.load(file)

moves_dict = {}
with open('./data/moves_dict.json', 'r', encoding='utf-8') as file:
    moves_dict = json.load(file)
moves_version = "1.0.3"


daily_object = {}
daily_object_day = None

def get_daily_object():
    global daily_object
    global daily_object_day
    today = date.today()
    if daily_object_day and today == daily_object_day:
        return daily_object
    random.seed(int(hashlib.md5(f"{today.year}{today.month}{today.day}".encode()).hexdigest()[:8], 16))
    species_id = random.choice(list(speciesdict.keys()))
    rspecies = random.choice(speciesdict[species_id])
    isShiny = 'normal'
    if random.randint(1, 50) == 1:
        isShiny = 'shiny'
    daily_object_day = today
    daily_object = {
        'name': rspecies.get('name', 'ERROR'),
        'img': rspecies.get('alt_internal_name', 'unown-qm'),
        'link': species_id,
        'shiny': isShiny
    }
    return daily_object



@app.route("/moves")
def get_moves():
    return render_template("moves.html")
@app.route("/cmoves")
def get_cmoves():
    return render_template("cmoves.html")
@app.route("/dmoves")
def get_dmoves():
    return render_template("dmoves.html")



@app.route("/api/moves")
def api_moves():
    return {'data': moves_dict}

@app.route("/api/moves/version")
def api_moves_version():
    return {'version': moves_version}

@app.route("/api/gary")
def api_gary():
    data = get_daily_object()
    return {'data': data}



with open('./data/species_picture.json', 'r', encoding='utf-8') as file:
    pokepics = json.load(file)

@app.route("/api/pokepic/<shiny>/<fake>/<id>")
def api_pokepic(shiny, fake, id):
    if fake == 'fake':
        picture = pokepics[id]
        if picture:
            if shiny == 'shiny':
                return picture['shiny']
            else:
                return picture['normal']
    else:
        return f'https://img.pokemondb.net/sprites/home/{shiny}/{id}.png'
    return ''



@app.route("/")
def read_root():
    return render_template("main.html")


with open('./data/fakemon_simple.json', 'r', encoding='utf-8') as file:
    fakemontable = json.load(file)
@app.route("/fakemon")
def get_fakemon():
    return render_template("fakemon.html", fakemon=fakemontable)

with open('./data/forms_simple.json', 'r', encoding='utf-8') as file:
    fakeformstable = json.load(file)
@app.route("/fakeforms")
def get_fakeforms():
    return render_template("fakeforms.html", fakeforms=fakeformstable)

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




@app.route("/staff")
def get_staff():
    return render_template("staff.html")
