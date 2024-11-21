import logging
from flask import Flask, render_template, send_from_directory
from flask_session import Session
from src.core.bcrypt import bcrypt
from src.web.handlers import error
from src.web.controllers.autenticacion import bp as bp_autenticacion
from src.web.controllers.usuarios import bp as bp_usuarios
from src.core import database
from src.core.config import config
from src.core import seeds
from src.web.handlers.funciones_auxiliares import (booleano_a_palabra,
                                                   fechahora,
                                                   fechahora_a_fecha,
                                                   mostrar_dato)
from src.web.controllers.miembro import bp as miembro_bp
from src.web.controllers.ecuestre import bp as ecuestre_bp
from src.web.controllers.jinetes_y_amazonas import bp as jinetes_y_amazonas_bp
from src.web.controllers.cobros import bp as cobros_bp
from src.web.controllers.pagos import bp as pagos_bp
from web.controllers.estadisticas import bp as estadisticas_bp
from src.web.controllers.anuncios import bp as anuncios_bp
from src.web.controllers.contacto import bp as contacto_bp
from src.web.api.api import bp as api_bp
from src.web.handlers.decoradores import esta_autenticado, tiene_permiso
from src.web.storage import storage
from src.web import helpers_jya

session = Session()

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.ERROR)


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

    app.register_blueprint(bp_autenticacion)
    app.register_blueprint(bp_usuarios)

    app.register_error_handler(404, error.error_not_found)
    app.register_error_handler(401, error.no_autorizado)
    app.register_error_handler(403, error.prohibido)

    app.jinja_env.add_extension('jinja2.ext.loopcontrols')
    app.jinja_env.globals.update(esta_autenticado=esta_autenticado)
    app.jinja_env.globals.update(tiene_permiso=tiene_permiso)
    app.jinja_env.globals.update(booleano_a_palabra=booleano_a_palabra)
    app.jinja_env.globals.update(fechahora_a_fecha=fechahora_a_fecha)
    app.jinja_env.globals.update(fechahora=fechahora)
    app.jinja_env.globals.update(documento_url=helpers_jya.archivo_url)
    app.jinja_env.globals.update(mostrar_dato=mostrar_dato)

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

    app.register_blueprint(pagos_bp)

    app.register_blueprint(estadisticas_bp)

    app.register_blueprint(anuncios_bp)
    
    app.register_blueprint(contacto_bp)

    app.register_blueprint(api_bp)

    return app

