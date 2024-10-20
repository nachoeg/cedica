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
    # raise Exception(f'{permiso} {permisos}')
    # raise Exception(f'{usuario.admin_sistema} {permisos}')
    return permiso in permisos

    # # forma de la expl de pr
    # # pero si usuario es None get_permisos(usuario) da error
    # return usuario is not None and permiso in permisos


def chequear_permiso(permiso):

    def decorator(f):

        @wraps(f)
        def wrapper(*args, **kwargs):
            if not tiene_permiso(session, permiso):
                return abort(403)

            return f(*args, **kwargs)

        return wrapper

    return decorator
