"""Flask instance initialization settings."""

import os
from dataclasses import dataclass
from functools import wraps
from dotenv import load_dotenv
from flask import flash, redirect, url_for, current_app, render_template
from babylab.src import api


class MissingEnvException(Exception):
    """If .env file is not found in user folder"""

    def __init__(self, envpath):
        msg = f".env file not found. Please, make sure to save your credentials in {envpath}"  # pylint: disable=line-too-long
        super().__init__(msg)


class MissingEnvToken(Exception):
    """If token is not provided under 'API_TEST_TOKEN' key."""

    def __init__(self):
        msg = "No token was found under the 'API_TEST_TOKEN' key in your .env file."  # pylint: disable=line-too-long
        super().__init__(msg)


def get_api_key():
    """Retrieve API credentials.

    Raises:
        MissingEnvException: If .en file is not located in ~/.env.
    """
    if os.getenv("GITHUB_ACTIONS") != "true":
        envpath = os.path.expanduser(os.path.join("~", ".env"))
        if not os.path.exists(envpath):
            raise MissingEnvException(envpath)
        load_dotenv(envpath)
    t = os.getenv("API_TEST_KEY")
    if not t:
        raise MissingEnvToken
    return t


@dataclass
class Config:
    """Initial settings."""

    testing: bool = False
    debug: bool = False
    api_key: str = "BADTOKEN"


@dataclass
class ProdConfig(Config):
    """Production settings."""


@dataclass
class DevConfig(Config):
    """Development settings."""

    testing: bool = True
    debug: bool = True
    api_key: str = get_api_key()


@dataclass
class TestConfig(Config):
    """Testing settings."""

    testing: bool = True
    api_key: str = get_api_key()


configs = {
    "dev": DevConfig,
    "prod": ProdConfig,
    "test": TestConfig,
}


def token_required(f):
    """Require login"""

    @wraps(f)
    def decorated(*args, **kwargs):
        redcap_version = api.get_redcap_version(token=current_app.config["API_KEY"])
        if redcap_version:
            return f(*args, **kwargs)
        flash("Access restricted. Please, log in.", "error")
        return redirect(url_for("index", redcap_version=redcap_version))

    return decorated


def get_records_or_index(token: str):
    """Try to get REDCap records, redirect to index if failure."""
    redcap_version = api.get_redcap_version(token=token)
    try:
        records = api.Records(token=token)
    except Exception:  # pylint: disable=broad-exception-caught
        return render_template("index.html", redcap_version=redcap_version)
    return records
