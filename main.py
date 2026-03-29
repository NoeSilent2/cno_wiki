import json
import random
import hashlib
import sqlite3
from datetime import date
from flask import Flask, g, render_template, redirect, url_for, send_from_directory


app = Flask(__name__)
DATABASE = "data/wiki.db"

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico', max_age=31536000)



def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def get_random_species_db():
    db = get_db()

    row = db.execute("SELECT internal_name FROM species ORDER BY RANDOM() LIMIT 1").fetchone()

    if not row:
        return "unown"
    
    name = row['internal_name']
    
    return name

def get_species_db(name):
    if name == "random":
        name = get_random_species_db()
    db = get_db()
    query = "SELECT * FROM species WHERE LOWER(internal_name) = LOWER(?)"
    rows = db.execute(query, (name,)).fetchall()

    if not rows:
        query = "SELECT * FROM species WHERE national_pokedex_number = ?"
        rows = db.execute(query, (name,)).fetchall()
        if not rows:
            return None

    results = []
    for row in rows:
        base = dict(row)
        extra_data = {}
        if base.get("extra"):
            try:
                extra_data = json.loads(base["extra"])
            except json.JSONDecodeError:
                extra_data = {}
        
        base.pop("extra", None)

        results.append({**base, **extra_data})
    
    return results

@app.route("/species/<name>")
def db_species_specific(name):
    results = get_species_db(name)
    if not results:
        return redirect(url_for("get_species"))

    return render_template("species_specific.html", species_forms=results)
    
    

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
    db = get_db()
    count = db.execute("SELECT COUNT(DISTINCT alt_internal_name) FROM species").fetchone()[0]
    offset = random.randint(0, count - 1)
    species_id = db.execute("SELECT DISTINCT alt_internal_name FROM species LIMIT 1 OFFSET ?",(offset,)).fetchone()
    species = db.execute("SELECT name, internal_name, alt_internal_name FROM species WHERE alt_internal_name = ? LIMIT 1",(species_id["alt_internal_name"],)).fetchone()
    isShiny = 'normal'
    if random.randint(1, 50) == 1:
        isShiny = 'shiny'
    daily_object_day = today
    daily_object = {
        'name': species["name"],
        'img': species["alt_internal_name"],
        'link': species["internal_name"],
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



@app.route("/")
def read_root():
    return render_template("main.html")

table_keys = [
    "national_pokedex_number",
    "name",
    "types",
    "stats",
    "height",
    "weight",
    "internal_name",
    "catch_rate"
]
pokemon_type = {
    "Legendary" : 5,
    "Mythical" : 4,
    "PsuedoLegendary" : 3,
    "UltraBeast" : 2,
    "Fossil" : 1
}

def get_pokemon_with(key,value):
    db = get_db()
    query = "SELECT * FROM species"
    if key and value:
        query += f" WHERE {key} = {value}"
    query += " ORDER BY national_pokedex_number COLLATE NOCASE"
    rows = db.execute(query).fetchall()

    result = []
    for row in rows:
        base = dict(row)
        extra_data = {}
        if base.get("extra"):
            try:
                extra_data = json.loads(base["extra"])
            except json.JSONDecodeError:
                extra_data = {}
        base.pop("extra", None)
        merged = {**base, **extra_data}
        filtered = {k: merged[k] for k in table_keys if k in merged}
        result.append(filtered)
    
    return result


@app.route("/fakemon")
def get_fakemon():
    result = get_pokemon_with("is_fake", 1)
    return render_template("sp_fake.html", fakemon=result)

@app.route("/fakeforms")
def get_fakeforms():
    result = get_pokemon_with("is_fake_form", 1)
    return render_template("sp_forms.html", fakeforms=result)

@app.route("/fossilmons")
def get_fossils():
    result = get_pokemon_with("legendary", pokemon_type["Fossil"])
    return render_template("sp_fossils.html", fossils=result)

@app.route("/species")
def get_species():
    result = get_pokemon_with(None, None)

    return render_template("sp_all.html", species=result)




@app.route("/staff")
def get_staff():
    return render_template("staff.html")
