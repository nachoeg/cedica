from src.core.bcrypt import bcrypt
from src.core.database import db
from core.usuarios.usuario import Permiso, Rol, Usuario


# USUARIOS
def listar_usuarios(email_filtro, orden, ordenar_por, pagina, cant_por_pagina):
    usuarios = db.paginate(
        db.select(
            Usuario
            ).order_by(getattr(getattr(Usuario, ordenar_por), orden)()),
        page=pagina,
        per_page=cant_por_pagina,
        error_out=False)
    total = usuarios.total
    # usuarios = [usuario.to_dict() for usuario in usuarios.items]

    return (total, usuarios)


def crear_usuario(email, contraseña, alias, admin_sistema=False, id_roles=[]):
    contraseña_hash = bcrypt.generate_password_hash(contraseña).decode('utf-8')
    usuario = Usuario(email=email, contraseña=contraseña_hash, 
                      alias=alias, admin_sistema=admin_sistema)

    roles = roles_por_id(id_roles)
    # raise Exception(f'{roles}')
    usuario.roles = roles
    db.session.add(usuario)
    db.session.commit()

    return usuario


def actualizar_usuario(usuario, email, alias, admin_sistema, id_roles):
    usuario.email = email
    usuario.alias = alias
    usuario.admin_sistema = admin_sistema
    roles = roles_por_id(id_roles)
    usuario.roles = roles
    db.session.commit()


def actualizar_perfil(usuario, email, alias):
    usuario.email = email
    usuario.alias = alias
    db.session.commit()


def asignar_roles(usuario, roles):
    usuario.roles = roles


def asignar_rol(usuario, rol):
    usuario.roles.append(rol)
    db.session.commit()

    return usuario


def eliminar_roles(usuario):
    for rol in usuario.roles:
        usuario.roles.pop(rol)


def usuario_por_id(id):
    usuario = db.get_or_404(Usuario, id)

    return usuario


def usuario_por_email(email):
    usuario = db.session.execute(db.select(Usuario).where(Usuario.email == email)).scalar_one_or_none()

    # # first() y one() devuelven una tupla, para que sea sólo el objeto tendría que usar scalars
    # usuario = db.session.scalars(db.select(Usuario).where(Usuario.email == email)).first()

    return usuario


def usuario_por_email_y_contraseña(email, contraseña):
    usuario = usuario_por_email(email)

    if usuario and bcrypt.check_password_hash(usuario.contraseña, contraseña):
        return usuario

    return None


# ROLES
def crear_rol(**kwargs):
    rol = Rol(**kwargs)
    db.session.add(rol)
    db.session.commit()

    return rol


def asignar_permiso(rol, permiso):
    rol.permisos.append(permiso)
    db.session.commit()

    return rol


def roles_por_id(ids):
    ids = [int(id) for id in ids]
    roles = db.session.execute(db.select(Rol).where(Rol.id.in_(ids))).unique().scalars().all()
    # raise Exception(f'{roles} {ids}')
    return roles


def roles_por_usuario(id):
    roles = db.session.execute(db.select(Rol).join(Usuario.roles.and_(Usuario.id == id))).unique().scalars().all()

    return roles


# PERMISOS
def crear_permiso(**kwargs):
    permiso = Permiso(**kwargs)
    db.session.add(permiso)
    db.session.commit()

    return permiso


def get_permisos(usuario):
    """Devuelve una lista con los nombres de los permisos del usuario que
    recibe por parámetro.
    """
    permisos = db.session.execute(db.select(Permiso.nombre).join(Permiso.roles).join(Rol.usuarios.and_(Usuario.id == usuario.id))).unique().scalars().all()

    return permisos
