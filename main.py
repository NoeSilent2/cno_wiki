import glob
import json
from flask import Flask, render_template


app = Flask(__name__)


@app.route("/")
def read_root():
    return render_template("main.html")

with open('./data/speciesdata.json', 'r', encoding='utf-8') as file:
    speciesdata = json.load(file)

@app.route("/species")
def get_species():
    return render_template("species.html", species=speciesdata)