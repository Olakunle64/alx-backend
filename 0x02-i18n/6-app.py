#!/usr/bin/env python3
"""Create a user system login"""
from flask import Flask, render_template, g
from flask_babel import Babel
from flask import request

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


app = Flask(__name__)
babel = Babel(app)


class Config():
    """configure available languages and timezone"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)


def get_user():
    """return user details"""
    user_id = request.args.get("login_as")
    try:
        user_id = int(user_id)
        if user_id in users.keys():
            return users.get(user_id)
    except Exception:
        return None


@babel.localeselector
def get_locale():
    """return the best matches LANGUAGE"""
    locale = request.args.get('locale')
    if not locale:
        user = getattr(g, "user", None)
        if user:
            locale = user.get("locale")
    if not locale:
        locale = request.accept_languages.best_match(app.config['LANGUAGES'])
    if not locale:
        locale = "en"
    if locale and locale in app.config["LANGUAGES"]:
        return locale


@app.before_request
def before_request():
    """a function to execute before any other function"""
    user = get_user()
    if user:
        setattr(g, "user", user)


@app.route("/")
def hello_world():
    """Greet the world"""
    # set a default welcome message
    user = getattr(g, "user", None)

    # check if the user exists
    return render_template(
        "6-index.html",
        user=user
    )


if __name__ == "__main__":
    """main function to run the app"""
    app.run(host="0.0.0.0", port=5000)
