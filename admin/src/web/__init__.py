from flask import Flask, render_template, send_from_directory
from src.web.handlers import error
from src.core import database
from src.core.config import config
from src.core import seeds
from src.web.controllers.jinetes_y_amazonas import bp as jinetes_y_amazonas_bp

def create_app(env="development", static_folder="../../static"):
    app = Flask(__name__, static_folder=static_folder)

    app.config.from_object(config[env])
    database.init_app(app)

    @app.route("/")
    def home():
        return render_template("pages/home.html")

    @app.route("/preline.js")
    def serve_preline_js():
        return send_from_directory("../../node_modules/preline/dist", "preline.js")

    app.register_error_handler(404, error.error_not_found)

    @app.cli.command(name="reset-db")
    def reset_db():
        database.reset()

    @app.cli.command(name="seeds-db")
    def seeds_db():
        seeds.run()

    app.register_blueprint(jinetes_y_amazonas_bp)

    return app
