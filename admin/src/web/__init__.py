from flask import Flask, render_template, send_from_directory
from src.web.handlers import error
from src.core import database
from src.core.config import config
from src.core import seeds
from src.web.controllers.ecuestre import bp as ecuestre_bp


def create_app(env="development", static_folder="../../static"):
    app = Flask(__name__, static_folder=static_folder)

    app.config.from_object(config[env])
    database.init_app(app)

    @app.route("/")
    def home():
        return render_template("pages/home.html")

    app.register_blueprint(ecuestre_bp)

    @app.route("/preline.js")
    def serve_preline_js():
        return send_from_directory("../../node_modules/preline/dist", "preline.js")

    @app.route("/jquery.js")
    def serve_jquery_js():
        return send_from_directory("../../node_modules/jquery/dist", "jquery.min.js")

    @app.route("/datatables.js")
    def serve_datatables_js():
        return send_from_directory(
            "../../node_modules/datatables.net/js", "dataTables.min.js"
        )

    app.register_error_handler(404, error.error_not_found)

    @app.cli.command(name="reset-db")
    def reset_db():
        database.reset()

    @app.cli.command(name="seeds-db")
    def seeds_db():
        seeds.run()

    return app
