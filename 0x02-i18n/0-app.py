#!/usr/bin/env python3
"""set up a basic flask app with a single route that output a template"""
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def hello_world():
    """Greet the world"""
    return render_template("0-index.html")


if __name__ == "__main__":
    """main function to run the app"""
    app.run(host="0.0.0.0", port=5000)
