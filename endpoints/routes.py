from flask import Flask, jsonify, render_template


app = Flask(__name__)

testdata = [
    {"id": 1026, "name": "Bamzu", "type1": "Grass", "type2": ""},
    {"id": 1027, "name": "Bambud", "type1": "Grass", "type2": "Steel"},
    {"id": 1028, "name": "Bamnom", "type1": "Grass", "type2": "Steel"}
]

@app.route("/species")
def get_species():
    return render_template("species.html", species=testdata)

