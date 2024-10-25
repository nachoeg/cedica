from functools import wraps
from flask import abort, session
from src.core.usuarios import get_permisos, usuario_por_email, usuario_por_id


def esta_autenticado(session):
    """Devuelve True si hay un usuario en la sesión actual."""
    return session.get('usuario') is not None


def sesion_iniciada_requerida(f):
    """Decorador que evalúa si hay un usuario autenticado, aborta con error 401
    en caso contrario.
    """

    @wraps(f)
    def wrapper(*args, **kwargs):
        if not esta_autenticado(session):
            return abort(401)

        return f(*args, **kwargs)

    return wrapper


def tiene_permiso(session, permiso):
    """Devuelve True si el usuario de la sesión tiene el permiso
    pasado por parámetro.
    """
    usuario = usuario_por_email(session.get('usuario'))
    if usuario is None:
        return False
    if usuario.admin_sistema:
        return True
    permisos = get_permisos(usuario)
    return permiso in permisos


def chequear_permiso(permiso):
    """Decorador que evalúa si un usuario tiene el permiso recibido
    por parámetro, aborta con error 403 en caso contrario.
    """

    def decorator(f):

        @wraps(f)
        def wrapper(*args, **kwargs):
            if not tiene_permiso(session, permiso):
                return abort(403)

            return f(*args, **kwargs)

        return wrapper

    return decorator


def es_usuario_de_sesion(session, id):
    return session.get('id') == id


def chequear_usuario_sesion(f):
    """Decorador que evalúa si el usuario cuyo id se toma de los parámetros
    de la función es el mismo que el usuario en la sesión actual.
    Aborta con error 403 en caso contrario.
    """

    @wraps(f)
    def wrapper(*args, **kwargs):
        id = kwargs['id']
        if not es_usuario_de_sesion(session, id):
            return abort(403)

        return f(*args, **kwargs)

    return wrapper


def no_modificar_admin(f):
    """Decorador que aborta con error 403 si el usuario
    cuyo id se recibe es admin.
    """

    @wraps(f)
    def wrapper(*args, **kwargs):
        id = kwargs['id']
        if usuario_por_id(id).admin_sistema:
            return abort(403)

        return f(*args, **kwargs)

    return wrapper
