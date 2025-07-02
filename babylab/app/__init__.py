"""Initialize app."""

import os
import datetime
from flask import Flask
from flask_babel import Babel, lazy_gettext
from flask_babel_js import BabelJS
from babylab.app.routes import appointments, general, participants, questionnaires
from babylab.app import config as conf


def create_app(env_: str = "prod"):
    """Create Flask app instance."""
    if env_ not in ["dev", "prod", "test"]:
        raise ValueError("`env` must be one of 'dev', 'prod', 'test'")

    app = Flask(__name__, template_folder="templates")

    # set up Babel for multilingual support
    Babel(app)

    # load initial settings
    app.config.from_object(conf.configs[env_])
    app.secret_key = os.urandom(24)
    app.permanent_session_lifetime = datetime.timedelta(minutes=10)
    app.config["API_KEY"] = conf.configs[env_].api_key
    app.config["TESTING"] = conf.configs[env_].testing
    app.config["RECORDS"] = None
    app.config["BABEL_TRANSLATION_DIRECTORIES"] = "../translations"
    app.config["BABEL_DEFAULT_LOCALE"] = "en"

    # import routes
    participants.ppt_routes(app)
    appointments.apt_routes(app)
    questionnaires.que_routes(app)
    general.general_routes(app)

    # set up Babel for multilingual support
    Babel(app, locale_selector=conf.get_locale, timezone_selector=None)
    babel_js = BabelJS(app)
    babel_js.init_app(app=app)

    @app.context_processor
    def inject_babel():
        return {"_": lazy_gettext}

    @app.context_processor
    def inject_locale():
        # This makes the function available directly, allowing you to call it in the template
        return {"get_locale": conf.get_locale}

    return app
