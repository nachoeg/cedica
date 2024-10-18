from src.core import usuarios


def cargar_permisos():
    permisos = {}
    permisos["permiso_usuario_listar"] = usuarios.crear_permiso(nombre="usuario_listar")
    permisos["permiso_usuario_crear"] = usuarios.crear_permiso(nombre="usuario_crear")
    permisos["permiso_usuario_eliminar"] = usuarios.crear_permiso(nombre="usuario_eliminar")
    permisos["permiso_usuario_actualizar"] = usuarios.crear_permiso(nombre="usuario_actualizar")
    permisos["permiso_usuario_mostrar"] = usuarios.crear_permiso(nombre="usuario_mostrar")

    permisos["permiso_miembro_listar"] = usuarios.crear_permiso(nombre="miembro_listar")
    permisos["permiso_miembro_crear"] = usuarios.crear_permiso(nombre="miembro_crear")
    permisos["permiso_miembro_eliminar"] = usuarios.crear_permiso(nombre="miembro_eliminar")
    permisos["permiso_miembro_actualizar"] = usuarios.crear_permiso(nombre="miembro_actualizar")
    permisos["permiso_miembro_mostrar"] = usuarios.crear_permiso(nombre="miembro_mostrar")

    return permisos


def cargar_roles():
    roles = {}
    roles["rol_tecnica"] = usuarios.crear_rol(nombre="Técnica")
    roles["rol_ecuestre"] = usuarios.crear_rol(nombre="Ecuestre")
    roles["rol_voluntariado"] = usuarios.crear_rol(nombre="Voluntariado")
    roles["rol_administracion"] = usuarios.crear_rol(nombre="Administración")

    permisos = cargar_permisos()

    # rol ADMINISTRACIÓN
    usuarios.asignar_permiso(roles["rol_administracion"], permisos["permiso_miembro_listar"])
    usuarios.asignar_permiso(roles["rol_administracion"], permisos["permiso_miembro_crear"])
    usuarios.asignar_permiso(roles["rol_administracion"], permisos["permiso_usuario_listar"])

    # rol ECUESTRE
    usuarios.asignar_permiso(roles["rol_ecuestre"], permisos["permiso_miembro_crear"])
    usuarios.asignar_permiso(roles["rol_ecuestre"], permisos["permiso_usuario_actualizar"])

    return roles


def cargar_usuarios():
    usuario1 = usuarios.crear_usuario(email="juan@mail.com", contraseña="123", alias="Juan")
    usuario2 = usuarios.crear_usuario(email="jorge@mail.com", contraseña="hola", alias="Jorge")
    usuario3 = usuarios.crear_usuario(email="maria@mail.com", contraseña="U.2", alias="Maria")
    usuario4 = usuarios.crear_usuario(email="claudia@mail.com", contraseña="hola", alias="Clau", admin_sistema=True)

    roles = cargar_roles()

    # Juan
    usuarios.asignar_rol(usuario1, roles["rol_administracion"])
    usuarios.asignar_rol(usuario1, roles["rol_ecuestre"])

    # María
    usuarios.asignar_rol(usuario3, roles["rol_ecuestre"])
