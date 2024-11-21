import math
from flask import Blueprint, current_app, render_template, request

from src.core.usuarios import listar_solicitudes
from src.web.handlers.decoradores import (chequear_permiso,
                                          sesion_iniciada_requerida)
from src.web.handlers.funciones_auxiliares import (convertir_a_entero,
                                                   palabra_a_booleano)


bp = Blueprint("solicitudes", __name__, url_prefix="/solicitudes")


@bp.route('/', methods=['GET'])
# @chequear_permiso('solicitud_listar')
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
