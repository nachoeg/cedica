from flask import Blueprint, render_template, request, redirect, url_for, flash
from src.web.handlers.funciones_auxiliares import convertir_a_entero
from src.web.handlers.decoradores import sesion_iniciada_requerida
from src.core.contacto import (
    listar_consultas,
    listar_estados_consultas,
    obtener_consulta,
    eliminar_consulta,
    archivar_consulta,
    desarchivar_consulta)

bp = Blueprint('contacto', __name__, url_prefix='/contacto')

@bp.get("/")
@sesion_iniciada_requerida
def listar():
    """Lista las consultas de forma paginada, una cantidad de 6 por pagina, permite aplicar filtros y ordenar de manera
    ascendente y descendente por diversos campos"""
    orden = request.args.get("orden", "asc")
    ordenar_por = request.args.get("ordenar_por", "fecha")
    pagina = convertir_a_entero(request.args.get("pagina", 1))
    cant_por_pagina = int(request.args.get("cant_por_pagina", 6))
    estado_filtro = request.args.get("estado", "")
    archivado = request.args.get("archivado", True)

    contactos, cant_resultados = listar_consultas(estado_filtro, ordenar_por, orden, pagina, cant_por_pagina, archivado) 

    tipos_estados = listar_estados_consultas()

    cant_paginas = cant_resultados // cant_por_pagina
    if cant_resultados % cant_por_pagina != 0:
        cant_paginas += 1

    return render_template(
        "pages/contactos/listar.html",
        contactos=contactos,
        tipos_estados=tipos_estados,
        cant_resultados=cant_resultados,
        cant_paginas=cant_paginas,
        pagina=pagina,
        orden=orden,
        ordenar_por=ordenar_por,
        estado=estado_filtro,
        archivado=archivado
    )

@bp.get("/<int:id>/")
@sesion_iniciada_requerida
def ver(id: int):
    """
    Devuelve la vista de una consulta en particular con el id dado.
    """
    consulta = obtener_consulta(id)
    return render_template("pages/contactos/ver.html", consulta=consulta)

@bp.route('/<int:id>/eliminar', methods=['GET'])
def eliminar(id):
    """Permite eliminar una consulta del sistema, 
    toma el id y se lo envia la modulo de contacto para hacer efectiva la baja"""
    eliminar_consulta(id)
    flash("Consulta eliminado con exito.", 'success')
    return redirect(url_for('contacto.listar'))

@bp.route('/<int:id>/archivar', methods=['GET'])
def archivar(id):
    """Permite eliminar una consulta del sistema, 
    toma el id y se lo envia la modulo de contacto para hacer efectiva la baja"""
    archivar_consulta(id)
    flash("Consulta archivada con exito.", 'success')
    return redirect(url_for('contacto.listar'))

@bp.route('/<int:id>/desarchivar', methods=['GET'])
def desarchivar(id):
    """Permite eliminar una consulta del sistema, 
    toma el id y se lo envia la modulo de contacto para hacer efectiva la baja"""
    desarchivar_consulta(id)
    flash("Consulta movida a recibidos con exito.", 'success')
    return redirect(url_for('contacto.listar'))