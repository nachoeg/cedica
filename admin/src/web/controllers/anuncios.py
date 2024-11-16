from flask import render_template, request, redirect, url_for, flash
from flask import Blueprint
from src.web.handlers.decoradores import (
    sesion_iniciada_requerida,
    chequear_permiso)
from src.web.handlers.funciones_auxiliares import convertir_a_entero
from src.core.anuncios import listar_anuncios, crear_anuncio
from core.forms.anuncios_forms import AnuncioForm

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


@bp.route("/nuevo_anuncio", methods=["GET","POST"])
@sesion_iniciada_requerida
def nuevo_anuncio():
    """
    Controlador para crear un nuevo anuncio.
    """
    form = AnuncioForm()
    print(request)
    if form.validate_on_submit():
        titulo = form.titulo.data
        copete = form.copete.data
        contenido = form.contenido.data
        print(request)
        # crear_anuncio(titulo, copete, contenido, )
        return redirect(url_for("home"))
    
    return render_template("pages/anuncios/crear.html",
                           form=form, titulo="Crear anuncio")


def ver_anuncio():
    """
    Controlador que permite ver un anuncio.
    """

    return render_template("pages/anuncios/ver.html")
