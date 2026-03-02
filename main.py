from flask import Flask, render_template


app = Flask(__name__)


@app.route("/")
def read_root():
    return render_template("main.html")

testdata = [
    {"id": 1026, "name": "Bamzu", "type1": "Grass", "type2": ""},
    {"id": 1027, "name": "Bambud", "type1": "Grass", "type2": "Steel"},
    {"id": 1028, "name": "Bamnom", "type1": "Grass", "type2": "Steel"}
]

@app.route("/species")
def get_species():
    return render_template("species.html", species=testdata)