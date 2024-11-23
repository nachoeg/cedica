from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from src.core.forms.contacto_forms import HistorialForm
from src.web.handlers.funciones_auxiliares import convertir_a_entero
from src.web.handlers.decoradores import sesion_iniciada_requerida, chequear_permiso
from src.core.contacto import (
    listar_consultas,
    listar_estados_consultas,
    obtener_consulta,
    eliminar_consulta,
    archivar_consulta,
    desarchivar_consulta,
    actualizar_estado,
    listar_historial)


bp = Blueprint('contacto', __name__, url_prefix='/contacto')


@chequear_permiso("consulta_listar")
@sesion_iniciada_requerida
def listar(titulo, archivado):
    """Lista las consultas de forma paginada, una cantidad de 6 por pagina, permite aplicar filtros y ordenar de manera
    ascendente y descendente por diversos campos"""
    cant_filas = current_app.config.get("TABLA_CANT_FILAS")
    orden = request.args.get("orden", "asc")
    ordenar_por = request.args.get("ordenar_por", "fecha")
    pagina = convertir_a_entero(request.args.get("pagina", 1))
    cant_por_pagina = int(request.args.get("cant_por_pagina", cant_filas))
    estado_filtro = request.args.get("estado", "")

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
        titulo=titulo,
        archivado=archivado
    )


@bp.get("/")
@chequear_permiso("consulta_listar")
@sesion_iniciada_requerida
def listar_recibidos():
    return listar(titulo="Consultas recibidas", archivado=False)
    

@bp.get("/archivados")
@chequear_permiso("consulta_listar")
@sesion_iniciada_requerida
def listar_archivados():
    return listar(titulo="Consultas archivadas", archivado=True)


@bp.route("/<int:id>/", methods=['GET', 'POST'])
@chequear_permiso("consulta_mostrar")
@sesion_iniciada_requerida
def ver(id: int):
    """
    Devuelve la vista de una consulta en particular con el id dado.
    """
    consulta = obtener_consulta(id)
    form = HistorialForm(obj=consulta)
    form.estado.choices = [estado for estado in listar_estados_consultas()]

    if request.method == "POST" and form.validate_on_submit():
        estado = form.estado.data
        comentario = form.comentario.data
        usuario = session.get('alias')
        actualizar_estado(id, estado, comentario, usuario)
        flash("Estado actualizado con éxito.", 'success')
        return redirect(url_for('contacto.listar_recibidos'))

    return render_template("pages/contactos/ver.html", form=form, consulta=consulta)      


@bp.route('/<int:id>/eliminar', methods=['GET'])
@chequear_permiso("consulta_eliminar")
@sesion_iniciada_requerida
def eliminar(id):
    """Permite eliminar una consulta del sistema, 
    toma el id y se lo envia la modulo de contacto para hacer efectiva la baja"""
    eliminar_consulta(id)
    flash("Consulta eliminado con exito.", 'success')
    return redirect(url_for('contacto.listar_recibidos'))


@bp.route('/<int:id>/archivar', methods=['GET'])
@chequear_permiso("consulta_actualizar")
@sesion_iniciada_requerida
def archivar(id):
    """Permite eliminar una consulta del sistema, 
    toma el id y se lo envia la modulo de contacto para hacer efectiva la baja"""
    archivar_consulta(id)
    flash("Consulta archivada con exito.", 'success')
    return redirect(url_for('contacto.listar_recibidos'))


@bp.route('/<int:id>/desarchivar', methods=['GET'])
@chequear_permiso("consulta_actualizar")
@sesion_iniciada_requerida
def desarchivar(id):
    """Permite eliminar una consulta del sistema, 
    toma el id y se lo envia la modulo de contacto para hacer efectiva la baja"""
    desarchivar_consulta(id)
    flash("Consulta movida a recibidos con exito.", 'success')
    return redirect(url_for('contacto.listar_recibidos'))


@bp.route('/<int:id>/listar_historial', methods=['GET'])
@chequear_permiso("consulta_mostrar")
@sesion_iniciada_requerida
def historial(id):
    """Permite listar el historial de estado
    por los que paso la consultas"""
    cant_filas = current_app.config.get("TABLA_CANT_FILAS")
    pagina = convertir_a_entero(request.args.get("pagina", 1))
    cant_por_pagina = int(request.args.get("cant_por_pagina", cant_filas))

    estados, cant_resultados = listar_historial(id, pagina, cant_por_pagina)

    cant_paginas = cant_resultados // cant_por_pagina
    if cant_resultados % cant_por_pagina != 0:
        cant_paginas += 1

    return render_template(
        "pages/contactos/listar_historial.html",
        estados=estados,
        cant_resultados=cant_resultados,
        cant_paginas=cant_paginas,
        pagina=pagina,
        consulta=id
    )