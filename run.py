"""Run app."""

from waitress import serve
from babylab.app import create_app

app = create_app(env_="prod")

if __name__ == "__main__":
    serve(app, host="127.0.0.1", port="5000")
