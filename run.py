"""Run app."""

# from waitress import serve
from flaskwebgui import FlaskUI
from babylab.app import create_app

app = create_app(env_="prod")
ui = FlaskUI(app=app, server="flask", port=5000, fullscreen=True)

if __name__ == "__main__":
    # serve(app, host="127.0.0.1", port="5000")
    ui.run()
