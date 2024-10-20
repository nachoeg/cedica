from src.core import usuarios


def cargar_permisos():
    permisos = {}
    permisos["permiso_usuario_listar"] = usuarios.crear_permiso(nombre="usuario_listar")
    permisos["permiso_usuario_mostrar"] = usuarios.crear_permiso(nombre="usuario_mostrar")
    permisos["permiso_usuario_crear"] = usuarios.crear_permiso(nombre="usuario_crear")
    permisos["permiso_usuario_actualizar"] = usuarios.crear_permiso(nombre="usuario_actualizar")
    permisos["permiso_usuario_eliminar"] = usuarios.crear_permiso(nombre="usuario_eliminar")

    permisos["permiso_miembro_listar"] = usuarios.crear_permiso(nombre="miembro_listar")
    permisos["permiso_miembro_crear"] = usuarios.crear_permiso(nombre="miembro_crear")
    permisos["permiso_miembro_eliminar"] = usuarios.crear_permiso(nombre="miembro_eliminar")
    permisos["permiso_miembro_actualizar"] = usuarios.crear_permiso(nombre="miembro_actualizar")
    permisos["permiso_miembro_mostrar"] = usuarios.crear_permiso(nombre="miembro_mostrar")

    permisos["permiso_pago_listar"] = usuarios.crear_permiso(nombre="pago_listar")
    permisos["permiso_pago_crear"] = usuarios.crear_permiso(nombre="pago_crear")
    permisos["permiso_pago_eliminar"] = usuarios.crear_permiso(nombre="pago_eliminar")
    permisos["permiso_pago_actualizar"] = usuarios.crear_permiso(nombre="pago_actualizar")
    permisos["permiso_pago_mostrar"] = usuarios.crear_permiso(nombre="pago_mostrar")

    permisos["permiso_jya_listar"] = usuarios.crear_permiso(nombre="jya_listar")
    permisos["permiso_jya_crear"] = usuarios.crear_permiso(nombre="jya_crear")
    permisos["permiso_jya_eliminar"] = usuarios.crear_permiso(nombre="jya_eliminar")
    permisos["permiso_jya_actualizar"] = usuarios.crear_permiso(nombre="jya_actualizar")
    permisos["permiso_jya_mostrar"] = usuarios.crear_permiso(nombre="jya_mostrar")

    permisos["permiso_cobro_listar"] = usuarios.crear_permiso(nombre="cobro_listar")
    permisos["permiso_cobro_crear"] = usuarios.crear_permiso(nombre="cobro_crear")
    permisos["permiso_cobro_eliminar"] = usuarios.crear_permiso(nombre="cobro_eliminar")
    permisos["permiso_cobro_actualizar"] = usuarios.crear_permiso(nombre="cobro_actualizar")
    permisos["permiso_cobro_mostrar"] = usuarios.crear_permiso(nombre="cobro_mostrar")

    permisos["permiso_ecuestre_listar"] = usuarios.crear_permiso(nombre="ecuestre_listar")
    permisos["permiso_ecuestre_crear"] = usuarios.crear_permiso(nombre="ecuestre_crear")
    permisos["permiso_ecuestre_eliminar"] = usuarios.crear_permiso(nombre="ecuestre_eliminar")
    permisos["permiso_ecuestre_actualizar"] = usuarios.crear_permiso(nombre="ecuestre_actualizar")
    permisos["permiso_ecuestre_mostrar"] = usuarios.crear_permiso(nombre="ecuestre_mostrar")

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
    usuarios.asignar_permiso(roles["rol_administracion"], permisos["permiso_miembro_mostrar"])
    usuarios.asignar_permiso(roles["rol_administracion"], permisos["permiso_miembro_crear"])
    usuarios.asignar_permiso(roles["rol_administracion"], permisos["permiso_miembro_actualizar"])
    usuarios.asignar_permiso(roles["rol_administracion"], permisos["permiso_miembro_eliminar"])

    usuarios.asignar_permiso(roles["rol_administracion"], permisos["permiso_pago_listar"])
    usuarios.asignar_permiso(roles["rol_administracion"], permisos["permiso_pago_mostrar"])
    usuarios.asignar_permiso(roles["rol_administracion"], permisos["permiso_pago_crear"])
    usuarios.asignar_permiso(roles["rol_administracion"], permisos["permiso_pago_actualizar"])
    usuarios.asignar_permiso(roles["rol_administracion"], permisos["permiso_pago_eliminar"])

    usuarios.asignar_permiso(roles["rol_administracion"], permisos["permiso_jya_listar"])
    usuarios.asignar_permiso(roles["rol_administracion"], permisos["permiso_jya_mostrar"])
    usuarios.asignar_permiso(roles["rol_administracion"], permisos["permiso_jya_crear"])
    usuarios.asignar_permiso(roles["rol_administracion"], permisos["permiso_jya_actualizar"])
    usuarios.asignar_permiso(roles["rol_administracion"], permisos["permiso_jya_eliminar"])

    usuarios.asignar_permiso(roles["rol_administracion"], permisos["permiso_cobro_listar"])
    usuarios.asignar_permiso(roles["rol_administracion"], permisos["permiso_cobro_mostrar"])
    usuarios.asignar_permiso(roles["rol_administracion"], permisos["permiso_cobro_crear"])
    usuarios.asignar_permiso(roles["rol_administracion"], permisos["permiso_cobro_actualizar"])
    usuarios.asignar_permiso(roles["rol_administracion"], permisos["permiso_cobro_eliminar"])

    usuarios.asignar_permiso(roles["rol_administracion"], permisos["permiso_ecuestre_listar"])
    usuarios.asignar_permiso(roles["rol_administracion"], permisos["permiso_ecuestre_mostrar"])

    # rol ECUESTRE
    usuarios.asignar_permiso(roles["rol_ecuestre"], permisos["permiso_jya_listar"])
    usuarios.asignar_permiso(roles["rol_ecuestre"], permisos["permiso_jya_mostrar"])

    usuarios.asignar_permiso(roles["rol_ecuestre"], permisos["permiso_ecuestre_listar"])
    usuarios.asignar_permiso(roles["rol_ecuestre"], permisos["permiso_ecuestre_mostrar"])
    usuarios.asignar_permiso(roles["rol_ecuestre"], permisos["permiso_ecuestre_crear"])
    usuarios.asignar_permiso(roles["rol_ecuestre"], permisos["permiso_ecuestre_actualizar"])
    usuarios.asignar_permiso(roles["rol_ecuestre"], permisos["permiso_ecuestre_eliminar"])

    # rol TÉCNICA
    usuarios.asignar_permiso(roles["rol_tecnica"], permisos["permiso_jya_listar"])
    usuarios.asignar_permiso(roles["rol_tecnica"], permisos["permiso_jya_mostrar"])
    usuarios.asignar_permiso(roles["rol_tecnica"], permisos["permiso_jya_crear"])
    usuarios.asignar_permiso(roles["rol_tecnica"], permisos["permiso_jya_actualizar"])
    usuarios.asignar_permiso(roles["rol_tecnica"], permisos["permiso_jya_eliminar"])

    usuarios.asignar_permiso(roles["rol_tecnica"], permisos["permiso_cobro_listar"])
    usuarios.asignar_permiso(roles["rol_tecnica"], permisos["permiso_cobro_mostrar"])

    usuarios.asignar_permiso(roles["rol_tecnica"], permisos["permiso_ecuestre_listar"])
    usuarios.asignar_permiso(roles["rol_tecnica"], permisos["permiso_ecuestre_mostrar"])

    return roles


def cargar_usuarios():

    usuarios.crear_usuario(email="admin@mail.com", contraseña="admin", alias="Clau", admin_sistema=True)

    todos_los_roles = usuarios.crear_usuario(email="roles@mail.com", contraseña="3.roles", alias="Juan")
    ecuestre = usuarios.crear_usuario(email="ecuestre@mail.com", contraseña="ecuestre", alias="Jorge")
    tecnica = usuarios.crear_usuario(email="tecnica@mail.com", contraseña="tecnica", alias="Maria")
    administracion = usuarios.crear_usuario(email="administracion@mail.com", contraseña="administracion", alias="Néstor")

    roles = cargar_roles()

    # Todos los roles - Juan
    usuarios.asignar_rol(todos_los_roles, roles["rol_administracion"])
    usuarios.asignar_rol(todos_los_roles, roles["rol_ecuestre"])
    usuarios.asignar_rol(todos_los_roles, roles["rol_tecnica"])
    usuarios.asignar_rol(todos_los_roles, roles["rol_voluntariado"])

    # Ecuestre - Jorge
    usuarios.asignar_rol(ecuestre, roles["rol_ecuestre"])

    # Técnica - María
    usuarios.asignar_rol(tecnica, roles["rol_tecnica"])

    # Administración - Néstor
    usuarios.asignar_rol(administracion, roles["rol_administracion"])
