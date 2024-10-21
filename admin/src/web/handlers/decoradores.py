from functools import wraps
from flask import abort, session
from core.usuarios import get_permisos, usuario_por_email


def esta_autenticado(session):
    return session.get('usuario') is not None


def sesion_iniciada_requerida(f):

    @wraps(f)
    def wrapper(*args, **kwargs):
        if not esta_autenticado(session):
            return abort(401)

        return f(*args, **kwargs)

    return wrapper


def tiene_permiso(session, permiso):
    usuario = usuario_por_email(session.get('usuario'))
    if usuario is None:
        return False
    if usuario.admin_sistema:
        return True
    permisos = get_permisos(usuario)
    return permiso in permisos


def chequear_permiso(permiso):

    def decorator(f):

        @wraps(f)
        def wrapper(*args, **kwargs):
            if not tiene_permiso(session, permiso):
                return abort(403)

            return f(*args, **kwargs)

        return wrapper

    return decorator


def es_el_mismo(session, id):
    return session.get('id') == id


def chequear_usuario():

    def decorator(f):

        @wraps(f)
        def wrapper(*args, **kwargs):
            id = kwargs['id']
            if not es_el_mismo(session, id):
                return abort(403)

            return f(*args, **kwargs)

        return wrapper

    return decorator
