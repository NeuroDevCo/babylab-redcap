"""Initialize app."""

import os
import datetime
from flask import Flask, request
from flask_babel import Babel
from babylab.app.routes import appointments, general, participants, questionnaires
from babylab.app import config


def get_locale():
    """Try to guess the language from the user accept
    header the browser transmits.  We support de/fr/en in this
    example. The best match wins.

    Returns:
        _type_: _description_
    """
    return request.accept_languages.best_match(["en", "es", "ca"])


def create_app(env_: str = "prod"):
    """Create Flask app instance."""
    if env_ not in ["dev", "prod", "test"]:
        raise ValueError("`env` must be one of 'dev', 'prod', 'test'")

    app = Flask(__name__, template_folder="templates")
    # load initial settings
    app.config.from_object(config.configs[env_])
    app.secret_key = os.urandom(24)
    app.permanent_session_lifetime = datetime.timedelta(minutes=10)
    app.config["API_KEY"] = config.configs[env_].api_key
    app.config["TESTING"] = config.configs[env_].testing
    app.config["RECORDS"] = None
    app.config["BABEL_TRANSLATION_DIRECTORIES"] = "translations"

    # set up Babel for multilingual support
    Babel(app, locale_selector=get_locale, timezone_selector=None)

    @app.context_processor
    def _():
        """Make get _locale available in Jinja2 template."""
        return {"get_locale": config.get_locale}

    # import routes
    participants.ppt_routes(app)
    appointments.apt_routes(app)
    questionnaires.que_routes(app)
    general.general_routes(app)

    return app
