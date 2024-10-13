from functools import wraps
from flask import abort, session


def esta_autenticado(session):
    return session.get('usuario') is not None


def sesion_iniciada_requerida(f):

    @wraps(f)
    def wrapper(*args, **kwargs):
        if not esta_autenticado(session):
            return abort(401)

        return f(*args, **kwargs)

    return wrapper
