from flask import render_template, request, redirect, url_for, flash
from flask import Blueprint
from src.web.handlers.decoradores import (
    sesion_iniciada_requerida,
    chequear_permiso)
from src.web.handlers.funciones_auxiliares import convertir_a_entero
from src.core.anuncios import listar_anuncios

bp = Blueprint("anuncios", __name__, url_prefix="/anuncios")


@bp.get("/")
@sesion_iniciada_requerida
def listar():
    """
    Controlador que lista todos los anuncios del sistema.
    """
    pagina = convertir_a_entero(request.args.get("pagina", 1))
    cant_por_pag = convertir_a_entero(request.args.get("por_pag", 6))

    anuncios = listar_anuncios()
    cant_resultados = 3
    cant_paginas = cant_resultados // cant_por_pag
    if cant_resultados % cant_por_pag != 0:
        cant_paginas += 1

    return render_template(
        "pages/anuncios/listar.html",
        anuncios=anuncios,
        cant_resultados=cant_resultados,
        cant_paginas=cant_paginas,
        pagina=pagina,
    )
