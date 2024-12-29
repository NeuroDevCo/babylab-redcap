"""Flask instance initialization settings."""

import os
from dataclasses import dataclass
from dotenv import load_dotenv


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
