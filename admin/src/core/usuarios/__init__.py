from src.core.database import db
from core.usuarios.usuario import Permiso, Rol, Usuario


# usuarios
def listar_usuarios():
    usuarios = Usuario.query.all()

    return usuarios


def crear_usuario(**kwargs):
    usuario = Usuario(**kwargs)
    db.session.add(usuario)
    db.session.commit()

    return usuario


def asignar_rol(usuario, rol):
    usuario.roles.append(rol)
    db.session.commit()

    return usuario


# agregar filtro por contraseña
def usuario_por_email_y_contraseña(email, contraseña):
    usuario = db.session.execute(db.select(Usuario).where(Usuario.email == email)).scalar_one_or_none()
    
    # # first() y one() devuelven una tupla, para que sea sólo el objeto tendría que usar scalars
    # usuario = db.session.scalars(db.select(Usuario).where(Usuario.email == email)).first()

    return usuario


# roles
def crear_rol(**kwargs):
    rol = Rol(**kwargs)
    db.session.add(rol)
    db.session.commit()

    return rol


def asignar_permiso(rol, permiso):
    rol.permisos.append(permiso)
    db.session.commit()

    return rol


# permisos
def crear_permiso(**kwargs):
    permiso = Permiso(**kwargs)
    db.session.add(permiso)
    db.session.commit()

    return permiso
