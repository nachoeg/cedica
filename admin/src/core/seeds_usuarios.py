from datetime import datetime
from src.core import usuarios


def cargar_permisos():
    permisos = {}
    permisos["permiso_usuario_listar"] = usuarios.crear_permiso(nombre="usuario_listar")
    permisos["permiso_usuario_mostrar"] = usuarios.crear_permiso(nombre="usuario_mostrar")
    permisos["permiso_usuario_crear"] = usuarios.crear_permiso(nombre="usuario_crear")
    permisos["permiso_usuario_actualizar"] = usuarios.crear_permiso(nombre="usuario_actualizar")
    permisos["permiso_usuario_bloquear"] = usuarios.crear_permiso(nombre="usuario_bloquear")
    permisos["permiso_usuario_activar"] = usuarios.crear_permiso(nombre="usuario_activar")
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

    usuarios.crear_usuario(email="admin@mail.com", contraseña="admin", alias="Clau", admin_sistema=True, creacion=datetime(2022, 3, 12))

    usuarios.crear_usuario(email="admin2@mail.com", contraseña="admin2", alias="Ale", admin_sistema=True, creacion=datetime(2021, 5, 29, 15, 23))

    todos_los_roles = usuarios.crear_usuario(email="roles@mail.com", contraseña="4.roles", alias="Ana", creacion=datetime(1992, 1, 17))
    administracion = usuarios.crear_usuario(email="administracion@mail.com", contraseña="administracion", alias="Juan", creacion=datetime(1999, 4, 23))
    ecuestre = usuarios.crear_usuario(email="ecuestre@mail.com", contraseña="ecuestre", alias="Pablo", creacion=datetime(2024, 10, 23))
    tecnica = usuarios.crear_usuario(email="tecnica@mail.com", contraseña="tecnica", alias="Maria", creacion=datetime(2021, 5, 29, 12, 37))
    voluntariado = usuarios.crear_usuario(email="voluntariado@mail.com", contraseña="voluntariado", alias="Néstor", creacion=datetime(2023, 5, 29))
    sin_roles = usuarios.crear_usuario(email="sinroles@mail.com", contraseña="sin_roles", alias="Sandra", creacion=datetime(2005, 12, 25))
    ecuestre1 = usuarios.crear_usuario(email="ecuestre1@mail.com", contraseña="ecuestre1", alias="Gloria", creacion=datetime(2024, 10, 23))
    ecuestre2 = usuarios.crear_usuario(email="ecuestre2@mail.com", contraseña="ecuestre2", alias="Leandro", creacion=datetime(2024, 10, 23))
    ecuestre3 = usuarios.crear_usuario(email="ecuestre3@mail.com", contraseña="ecuestre3", alias="Vanesa", creacion=datetime(2024, 10, 23))
    ecuestre4 = usuarios.crear_usuario(email="ecuestre4@mail.com", contraseña="ecuestre4", alias="Kimey", creacion=datetime(2024, 10, 23))
    ecuestre5 = usuarios.crear_usuario(email="ecuestre5@mail.com", contraseña="ecuestre5", alias="Lorena", creacion=datetime(2024, 10, 23))
    ecuestre6 = usuarios.crear_usuario(email="ecuestre6@mail.com", contraseña="ecuestre6", alias="Julia", creacion=datetime(2024, 10, 23))

    roles = cargar_roles()

    # Todos los roles - Juan
    usuarios.asignar_rol(todos_los_roles, roles["rol_administracion"])
    usuarios.asignar_rol(todos_los_roles, roles["rol_ecuestre"])
    usuarios.asignar_rol(todos_los_roles, roles["rol_tecnica"])
    usuarios.asignar_rol(todos_los_roles, roles["rol_voluntariado"])

    # Ecuestre - Jorge
    usuarios.asignar_rol(ecuestre, roles["rol_ecuestre"])

    # Otros usuarios con rol Ecuestre
    usuarios.asignar_rol(ecuestre1, roles["rol_ecuestre"])
    usuarios.asignar_rol(ecuestre2, roles["rol_ecuestre"])
    usuarios.asignar_rol(ecuestre3, roles["rol_ecuestre"])
    usuarios.asignar_rol(ecuestre4, roles["rol_ecuestre"])
    usuarios.asignar_rol(ecuestre5, roles["rol_ecuestre"])
    usuarios.asignar_rol(ecuestre6, roles["rol_ecuestre"])

    # Técnica - María
    usuarios.asignar_rol(tecnica, roles["rol_tecnica"])

    # Administración - Néstor
    usuarios.asignar_rol(administracion, roles["rol_administracion"])
