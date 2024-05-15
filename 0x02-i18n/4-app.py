#!/usr/bin/env python3
"""set up a basic flask app with a single route that
    output a template and also use use Babel to configure
    the default locale and timezone.
"""
from flask import Flask, render_template
from flask_babel import Babel, _
from flask import request

app = Flask(__name__)
babel = Babel(app)


class Config():
    """configure available languages and timezone"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)


@babel.localeselector
def get_locale():
    """return the best matches LANGUAGE"""
    locale = request.args.get('locale')
    if locale and locale in app.config["LANGUAGES"]:
        return locale
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route("/")
def hello_world():
    """Greet the world"""
    return render_template(
        "4-index.html",
    )


if __name__ == "__main__":
    """main function to run the app"""
    app.run(host="0.0.0.0", port=5000)
