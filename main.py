from flask import Flask, render_template
from endpoints import api_bp


app = Flask(__name__)


app.register_blueprint(api_bp)


@app.route("/")
def read_root():
    return render_template("main.html")
