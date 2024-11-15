from datetime import datetime

from src.core.bcrypt import bcrypt
from src.core.database import db
from core.usuarios.usuario import Permiso, Rol, Usuario


# USUARIOS
def listar_usuarios(orden, ordenar_por, pagina, cant_por_pagina,
                    email_filtro, activo_filtro, rol_filtro):
    """Devuelve una tupla que contiene un listado paginado
    de usuarios, filtrado y ordenado, y la cantidad total de
    usuarios que genera la consulta.
    """
    email_filtro = Usuario.email.ilike(f"%{email_filtro}%")
    activo_filtro = (Usuario.activo == activo_filtro 
                     if activo_filtro != '' else True)
    if rol_filtro == '':
        rol_filtro = True
    elif rol_filtro == 'Sin rol':
        rol_filtro = Rol.id.is_(None)
    else:
        rol_filtro = Rol.nombre == rol_filtro

    usuarios = db.paginate(
        db.select(Usuario).distinct().join(
            Usuario.roles, isouter=True
            ).where(email_filtro, activo_filtro, rol_filtro
                    ).order_by(getattr(getattr(Usuario, ordenar_por), orden)()),
        page=pagina,
        per_page=cant_por_pagina,
        error_out=False)
    total = usuarios.total
    # usuarios = [usuario.to_dict() for usuario in usuarios.items]

    return (total, usuarios)


def crear_usuario(email, contraseña, alias, admin_sistema=False,
                  id_roles=[], creacion=datetime.now()):
    """Crea un objeto de tipo Usuario con los datos que recibe por
    parámetro y lo devuelve.
    """
    contraseña_hash = bcrypt.generate_password_hash(contraseña).decode('utf-8')
    email = email.lower()
    usuario = Usuario(email=email, contraseña=contraseña_hash, 
                      alias=alias, admin_sistema=admin_sistema,
                      creacion=creacion)
    if not admin_sistema:
        roles = roles_por_id(id_roles)
        usuario.roles = roles
    db.session.add(usuario)
    db.session.commit()

    return usuario


def asignar_contraseña(usuario, contraseña):
    """Asigna al usuario que recibe por parámetro la
    contraseña que también recibe como parámetro.
    """
    contraseña_hash = bcrypt.generate_password_hash(contraseña).decode('utf-8')
    usuario.contraseña = contraseña_hash
    db.session.commit()


def actualizar_usuario(usuario, email, alias, admin_sistema, id_roles):
    """Modifica los datos del usuario que recibe por parámetro con los
    datos en el resto de los parámetros.

    Parámetros:
    """
    usuario.email = email.lower()
    usuario.alias = alias
    usuario.admin_sistema = admin_sistema
    if admin_sistema:
        usuario.roles = []
    else:
        roles = roles_por_id(id_roles)
        usuario.roles = roles
    db.session.commit()


def actualizar_perfil(usuario, email, alias):
    """Modifica los datos del usuario que recibe por parámetro con los
    datos en el resto de los parámetros.

    Parámetros:
    """
    usuario.email = email.lower()
    usuario.alias = alias
    db.session.commit()


def asignar_rol(usuario, rol):
    """Agrega un rol a los roles del usuario
    pasado por parámetro.
    """
    usuario.roles.append(rol)
    db.session.commit()

    return usuario


def usuario_por_id(id):
    """Devuelve el usuario correspondiente al id pasado por
    parámetro. Si no lo encuentra levanta un error 404.
    """
    usuario = db.get_or_404(Usuario, id)

    return usuario


def usuario_por_id_none(id):
    """Devuelve el usuario correspondiente al id pasado por
    parámetro. Si no lo encuentra devuelve None.
    """
    usuario = db.session.execute(
        db.select(Usuario).where(Usuario.id == id)).scalar_one_or_none()
    return usuario


def usuario_por_email(email):
    """Devuelve el usuario correspondiente al email pasado por
    parámetro. Si no lo encuentra devuelve None.
    """
    usuario = db.session.execute(
        db.select(Usuario).where(Usuario.email == email)).scalar_one_or_none()

    return usuario


def usuario_por_alias(alias):
    return Usuario.query.filter_by(alias=alias).filter(Usuario.activo.is_(True)).first()


def usuario_por_email_y_contraseña(email, contraseña):
    """Devuelve el usuario correspondiente al email y contraseña
    pasados por parámetro.
    """
    usuario = usuario_por_email(email)

    if usuario and bcrypt.check_password_hash(usuario.contraseña, contraseña):
        return usuario

    return None


# ROLES
def crear_rol(**kwargs):
    """Crea un objeto de tipo Rol con los datos que recibe por
    parámetro y lo devuelve.
    """
    rol = Rol(**kwargs)
    db.session.add(rol)
    db.session.commit()

    return rol


def nombres_roles():
    """Devuelve una lista con los nombres de todos los roles
    en la base de datos.
    """
    roles = db.session.execute(db.select(Rol.nombre)).scalars().all()

    return roles


def asignar_permiso(rol, permiso):
    """Agrega un permiso a los permisos del rol
    pasado por parámetro.
    """
    rol.permisos.append(permiso)
    db.session.commit()

    return rol


def roles_por_id(ids):
    """Devuelve los roles correspondientes a los ids
    pasados por parámetro.
    """
    ids = [int(id) for id in ids]
    roles = db.session.execute(db.select(Rol).where(
        Rol.id.in_(ids))).unique().scalars().all()
    return roles


def roles_por_usuario(id):
    """Devuelve los roles del usuario cuyo id se recibe
    pasados por parámetro.
    """
    roles = db.session.execute(db.select(Rol).join(
        Usuario.roles.and_(Usuario.id == id))).unique().scalars().all()

    return roles


def get_roles():
    """Devuelve todos los roles."""
    roles = db.session.execute(db.select(Rol)).unique().scalars().all()

    return roles


# PERMISOS
def crear_permiso(**kwargs):
    """Crea un objeto de tipo Permiso con los datos que recibe por
    parámetro y lo devuelve.
    """
    permiso = Permiso(**kwargs)
    db.session.add(permiso)
    db.session.commit()

    return permiso


def nombres_permisos(usuario):
    """Devuelve una lista con los nombres de los permisos del usuario que
    recibe por parámetro.
    """
    permisos = db.session.execute(db.select(Permiso.nombre
                                            ).join(Permiso.roles
                                                   ).join(Rol.usuarios.and_(
                                                       Usuario.id == usuario.id
                                                       ))
                                  ).unique().scalars().all()

    return permisos
