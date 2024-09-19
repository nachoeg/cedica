from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_app(app):
    """Inicializa la base de datos con la aplicación de Flask."""
    db.init_app(app)
    config(app)

    return app


def config(app):
    """Configuración de hooks para la base de datos"""

    @app.teardown_appcontext
    def close_session(exception=None):
        db.session.remove()

    return app


def reset():
    """Resetea la base de datos"""
    print("🗑 Eliminando la base de datos...")
    db.drop_all()
    print("🆕 Creando base nuevamente...")
    db.create_all()
    print("✔ Hecho!")
