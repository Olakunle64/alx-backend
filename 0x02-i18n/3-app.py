#!/usr/bin/env python3
"""set up a basic flask app with a single route that
    output a template and also use use Babel to configure
    the default locale and timezone.
"""
from flask import Flask, render_template
from flask_babel import Babel
from flask import request

app = Flask(__name__)
babel = Babel(app)


@babel.localeselector
def get_locale() -> str:
    """return the best matches LANGUAGE"""
    return request.accept_languages.best_match(app.config['LANGUAGES'])


class Config():
    """configure available languages and timezone"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)


@app.route("/")
def hello_world() -> str:
    """Greet the world"""
    return render_template(
        "3-index.html")


if __name__ == "__main__":
    """main function to run the app"""
    app.run(host="0.0.0.0", port=5000)
