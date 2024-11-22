from flask import render_template, request, redirect, url_for, flash, session
from flask import Blueprint
from datetime import datetime
from src.web.handlers.decoradores import (
    sesion_iniciada_requerida,
    chequear_permiso)
from src.web.handlers.funciones_auxiliares import convertir_a_entero
from src.core.anuncios import (
    listar_anuncios, crear_anuncio, encontrar_anuncio, guardar_cambios,
    eliminar_anuncio, listar_estados)
from core.forms.anuncios_forms import NuevoAnuncioForm, EditarAnuncioForm

bp = Blueprint("anuncios", __name__, url_prefix="/anuncios")


@bp.get("/")
@sesion_iniciada_requerida
def listar():
    """
    Controlador que lista todos los anuncios del sistema.
    """
    orden = request.args.get("orden", "asc")
    ordenar_por = request.args.get("ordenar_por", "id")
    pagina = convertir_a_entero(request.args.get("pagina", 1))
    cant_por_pag = convertir_a_entero(request.args.get("por_pag", 6))
    titulo_filtro = request.args.get("titulo", "")
    autor_filtro = request.args.get("autor", "")
    estado_filtro = request.args.get("estado", "")
    despues_de_filtro = request.args.get("despues_de", "")
    antes_de_filtro = request.args.get("antes_de_filtro", "")

    anuncios, cant_resultados = listar_anuncios(
        titulo_filtro,
        autor_filtro,
        estado_filtro,
        despues_de_filtro,
        antes_de_filtro,
        ordenar_por,
        orden,
        pagina,
        cant_por_pag
    )

    estados = listar_estados()

    cant_paginas = cant_resultados // cant_por_pag
    if cant_resultados % cant_por_pag != 0:
        cant_paginas += 1

    return render_template(
        "pages/anuncios/listar.html",
        anuncios=anuncios,
        estados=estados,
        cant_resultados=cant_resultados,
        cant_paginas=cant_paginas,
        pagina=pagina,
        orden=orden,
        ordenar_por=ordenar_por,
        titulo_filtro=titulo_filtro,
        autor_filtro=autor_filtro,
        estado_filtro=estado_filtro,
        despues_de_filtro=despues_de_filtro,
        antes_de_filtro=antes_de_filtro
    )


@bp.route("/nuevo_anuncio", methods=["GET", "POST"])
@sesion_iniciada_requerida
def nuevo_anuncio():
    """
    Controlador para crear un nuevo anuncio.
    """
    form = NuevoAnuncioForm()

    if form.validate_on_submit():
        titulo = form.titulo.data
        copete = form.copete.data
        contenido = form.contenido.data
        id = session["id"]
        crear_anuncio(titulo, copete, contenido, id)

        return redirect(url_for("anuncios.listar"))

    return render_template("pages/anuncios/crear.html",
                           form=form, nuevo=True, titulo="Crear anuncio")


@bp.get("/<int:id>")
@sesion_iniciada_requerida
def ver_anuncio(id: int):
    """
    Controlador que permite ver un anuncio.
    """
    anuncio = encontrar_anuncio(id)
    return render_template("pages/anuncios/ver.html",
                           anuncio=anuncio)


@bp.route("/<int:id>/editar", methods=["GET", "POST"])
@sesion_iniciada_requerida
def editar_anuncio(id: int):
    """
    Controlador que permite editar un anuncio.
    """
    anuncio = encontrar_anuncio(id)
    form = EditarAnuncioForm(obj=anuncio)

    if request.method == "POST":
        if form.validate_on_submit():
            anuncio.titulo = form.titulo.data
            anuncio.copete = form.copete.data
            anuncio.contenido = form.contenido.data
            anuncio.estado = form.estado.data
            anuncio.fecha_ultima_actualizacion = datetime.now()
            if anuncio.estado == "pu":
                anuncio.fecha_publicacion = datetime.now()
            guardar_cambios()
            flash("Anuncio actualizado con éxito", "exito")
            return redirect(url_for("anuncios.ver_anuncio", id=id))

        else:
            flash("Error al actualizar el anuncio", "error")

    form.estado.data = anuncio.estado.name

    return render_template("/pages/anuncios/crear.html",
                           form=form,
                           nuevo=False,
                           titulo="Editar anuncio")


@bp.get("/<int:id>/eliminar")
@sesion_iniciada_requerida
def eliminar(id: int):
    """
    Controlador que gestiona la eliminación de un anuncio.
    """
    eliminar_anuncio(id)
    flash("Anuncio eliminado con éxito", "exito")

    return redirect(url_for("anuncios.listar"))
