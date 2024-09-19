from flask import Flask
from flask import render_template
from src.web.handlers import error
from src.core import database


def create_app(env="development", static_folder="../../static"):
    app = Flask(__name__, static_folder=static_folder)

    database.init_app(app)

    @app.route("/")
    def home():
        return render_template("home.html")
    
    app.register_error_handler(404, error.error_not_found)

    @app.cli.command(name="reset-db")
    def reset_db():
        database.reset()

    return app
