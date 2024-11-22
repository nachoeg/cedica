import math

from flask import (Blueprint, current_app, flash,
                   redirect, render_template, request, url_for)

from src.core.database import db
from src.core.usuarios import (crear_usuario, listar_solicitudes,
                               solicitud_por_id, usuario_por_email)
from src.web.handlers.decoradores import (chequear_permiso,
                                          sesion_iniciada_requerida)
from src.web.handlers.funciones_auxiliares import (convertir_a_entero,
                                                   palabra_a_booleano)


bp = Blueprint("solicitudes", __name__, url_prefix="/solicitudes")


@bp.route('/', methods=['GET'])
@chequear_permiso('solicitud_listar')
@sesion_iniciada_requerida
def listado_solicitudes():
    """Devuelve la vista de usuarios en la base de datos
    Los datos se envían paginados, filtrados y ordenados.
    """
    cant_filas = current_app.config.get("TABLA_CANT_FILAS")

    orden = request.args.get("orden", "asc")
    ordenar_por = request.args.get("ordenar_por", "id")
    pagina = convertir_a_entero(request.args.get("pagina", 1))
    cant_por_pagina = int(request.args.get("cant_por_pagina", cant_filas))
    email_filtro = request.args.get("email", "")
    aceptada_filtro = request.args.get("activo", "")

    # activo_filtro = palabra_a_booleano(activo_filtro)
    cant_resultados, solicitudes = listar_solicitudes(
        orden, ordenar_por, pagina, cant_por_pagina,
        email_filtro, palabra_a_booleano(aceptada_filtro),
        )

    cant_paginas = math.ceil(cant_resultados / cant_por_pagina)

    return render_template("pages/solicitudes/listado_solicitudes.html",
                           solicitudes=solicitudes,
                           cant_resultados=cant_resultados,
                           cant_paginas=cant_paginas,
                           pagina=pagina,
                           orden=orden,
                           ordenar_por=ordenar_por,
                           email_filtro=email_filtro,
                           aceptada_filtro=aceptada_filtro,
                           )


@bp.route('/<int:id>/aceptar', methods=['GET'])
@chequear_permiso('solicitud_aceptar')
@sesion_iniciada_requerida
def aceptar_solicitud(id):
    solicitud = solicitud_por_id(id)
    usuario = usuario_por_email(solicitud.email)
    if not solicitud.aceptada and usuario is None:
        # cambiar por una solicitud de ingresar alias que chequee unicidad
        alias = solicitud.email.split('@')[0]
        usuario = crear_usuario(email=solicitud.email, alias=alias,
                                sin_contraseña=True)
        solicitud.aceptada = True
        db.session.commit()
        flash(f'Se ha creado el usuario \
                Alias: {usuario.alias}, email: {usuario.email}', 'exito')
    else:
        flash(f'El usuario \
                Alias: {usuario.alias}, email: {usuario.email} \
                ya se encuentra activo', 'info')
    return redirect(url_for('solicitudes.listado_solicitudes'))


@bp.route('/<int:id>/eliminar', methods=['GET'])
@chequear_permiso('solicitud_eliminar')
@sesion_iniciada_requerida
def eliminar_solicitud(id):
    solicitud = solicitud_por_id(id)
    db.session.delete(solicitud)
    db.session.commit()
    flash(f'Se ha eliminado la solicitud \
              del email: {solicitud.email}', 'exito')
    return redirect(url_for('solicitudes.listado_solicitudes'))
