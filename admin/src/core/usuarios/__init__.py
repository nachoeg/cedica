from src.core.database import db
from core.usuarios.usuario import Usuario


def list_users():
    users = Usuario.query.all()

    return users


def create_user(**kwargs):
    user = Usuario(**kwargs)
    db.session.add(user)
    db.session.commit()

    return user
