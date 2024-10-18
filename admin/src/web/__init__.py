import logging
from flask import Flask, render_template, send_from_directory
from flask_session import Session
from src.core.bcrypt import bcrypt
from src.web.handlers import error
from src.web.controllers.autenticacion import bp as bp_autenticacion
from src.core import database
from src.core.config import config
from src.core import seeds
from .controllers.miembro import miembro_bp
from src.web.controllers.ecuestre import bp as ecuestre_bp
from src.web.controllers.jinetes_y_amazonas import bp as jinetes_y_amazonas_bp
from src.web.controllers.cobros import bp as cobros_bp
from src.web.controllers.pagos import pago_bp
from src.web.handlers.autenticacion import esta_autenticado, tiene_permiso
from src.web.storage import storage

session = Session()

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)


def create_app(env="development", static_folder="../../static"):
    app = Flask(__name__, static_folder=static_folder)
    app.config['SECRET_KEY'] = 'SecretKey'
    app.config.from_object(config[env])
    database.init_app(app)

    session.init_app(app)
    bcrypt.init_app(app)

    storage.init_app(app)

    @app.route("/")
    def home():
        return render_template("pages/home.html")

    @app.route("/preline.js")
    def serve_preline_js():
        return send_from_directory(
            "../../node_modules/preline/dist",
            "preline.js",
        )

    app.register_blueprint(bp_autenticacion)

    app.register_error_handler(404, error.error_not_found)
    app.register_error_handler(401, error.no_autorizado)
    app.register_error_handler(403, error.prohibido)

    app.jinja_env.globals.update(esta_autenticado=esta_autenticado)
    app.jinja_env.globals.update(tiene_permiso=tiene_permiso)

    @app.cli.command(name="reset-db")
    def reset_db():
        database.reset()

    @app.cli.command(name="seeds-db")
    def seeds_db():
        seeds.run()

    app.register_blueprint(jinetes_y_amazonas_bp)

    app.register_blueprint(ecuestre_bp)

    app.register_blueprint(miembro_bp)

    app.register_blueprint(cobros_bp)

    app.register_blueprint(pago_bp)

    return app
