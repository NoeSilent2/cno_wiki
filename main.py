import os
import json
import random
import hashlib
from datetime import datetime, date, timedelta
from flask import Flask, render_template, redirect, url_for, send_from_directory, make_response


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


gary_daily = '/tmp/gary_daily.json'

def get_daily_object():
    now = datetime.now(datetime.timezone.utc).date().isoformat

    if os.path.exists(gary_daily):
        try:
            with open(gary_daily, 'r') as file:
                data = json.load(file)
            
            if data.get('date') == now:
                return data['data']
        except (json.JSONDecodeError, KeyError, IOError):
            pass
    
    species_id = random.choice(list(speciesdict.keys()))
    new_data = random.choice(speciesdict[species_id])

    isShiny = 'normal'
    if random.randint(1, 50) == 1:
        isShiny = 'shiny'

    save_data = {}
    save_data['name'] = new_data.get('name', 'ERROR')
    save_data['img'] = new_data.get('alt_internal_name', 'unown-qm')
    save_data['link'] = species_id
    save_data['shiny'] = isShiny

    try:
        with open(gary_daily, 'w') as file:
            json.dump({
                'date': now,
                'object': save_data
            }, file)
    except IOError:
        pass
    
    return save_data

def daily_cache_duration():
    now = datetime.now(datetime.timezone.utc)
    tomorrow = datetime(now.year, now.month, now.day) + timedelta(days=1)
    seconds_until_midnight = (tomorrow - now).total_seconds()
    return int(seconds_until_midnight)



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
    daily_object = get_daily_object()
    cache_duration = daily_cache_duration()

    response = make_response({
        'object': daily_object,
        'date': datetime.now(datetime.timezone.utc).date().isoformat(),
        'expiration': cache_duration
    })
    
    response.headers['Cache-Control'] = f'public, max-age={cache_duration}'
    return response





@app.route("/")
def read_root():
    time = daily_cache_duration()
    response = render_template("main.html", pokemon=get_daily_object())
    return response, 200, {
        'Cache-Control': f'public, s-maxage={time}, must-revalidate'
    }


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
