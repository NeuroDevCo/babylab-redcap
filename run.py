"""Run app."""

from waitress import serve
from babylab.app import create_app

app = create_app(env="prod")

if __name__ == "__main__":
    # app.run(debug=False)
    serve(app, host="127.0.0.1", port="5000")
