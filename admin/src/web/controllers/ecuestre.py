from flask import Blueprint, render_template, request, redirect, url_for, flash
from src.core.ecuestre import (
    crear_ecuestre,
    eliminar_ecuestre,
    obtener_ecuestre,
    listar_tipos_de_jya,
    listar_ecuestres,
    guardar_cambios,
)
from src.core.ecuestre.ecuestre_form import EcuestreForm


bp = Blueprint("ecuestre", __name__, url_prefix="/ecuestre")


@bp.get("/")
def index():
    orden = request.args.get("orden", "asc")
    ordenar_por = request.args.get("ordenar_por", "id")
    pagina = int(request.args.get("pagina", 1))
    cant_por_pagina = int(request.args.get("cant_por_pagina", 10))
    nombre_filtro = request.args.get("nombre", "")
    tipo_jya_filtro = request.args.get("tipo_jya", "")

    ecuestres, cant_resultados = listar_ecuestres(
        nombre_filtro, tipo_jya_filtro, ordenar_por, orden, pagina, cant_por_pagina
    )

    tipos_jya = listar_tipos_de_jya()

    cant_paginas = cant_resultados // cant_por_pagina
    if cant_resultados % cant_por_pagina != 0:
        cant_paginas += 1

    return render_template(
        "pages/ecuestre/listar.html",
        ecuestres=ecuestres,
        tipos_jya=tipos_jya,
        cant_resultados=cant_resultados,
        cant_paginas=cant_paginas,
        pagina=pagina,
        orden=orden,
        ordenar_por=ordenar_por,
        tipo_jya_filtro=tipo_jya_filtro,
        nombre_filtro=nombre_filtro,
    )


@bp.get("/<int:id>/")
def ver(id: int):
    ecuestre = obtener_ecuestre(id)
    return render_template("pages/ecuestre/ver.html", ecuestre=ecuestre)


@bp.route("/crear/", methods=["GET", "POST"])
def crear():
    form = EcuestreForm()
    form.tipo_de_jya_id.choices = [(t.id, t.tipo) for t in listar_tipos_de_jya()]

    if form.validate_on_submit():
        nombre = form.nombre.data
        fecha_nacimiento = form.fecha_nacimiento.data
        sexo = form.sexo.data
        raza = form.raza.data
        pelaje = form.pelaje.data
        es_compra = form.es_compra.data == "True"
        fecha_ingreso = form.fecha_ingreso.data
        sede = form.sede.data
        tipo_de_jya_id = form.tipo_de_jya_id.data
        crear_ecuestre(
            nombre,
            fecha_nacimiento,
            sexo,
            raza,
            pelaje,
            es_compra,
            fecha_ingreso,
            sede,
            tipo_de_jya_id,
        )
        return redirect(url_for("ecuestre.index"))

    return render_template("pages/ecuestre/formulario.html", form=form)


@bp.route("/<int:id>/editar/", methods=["GET", "POST"])
def editar(id: int):
    ecuestre = obtener_ecuestre(id)
    form = EcuestreForm(obj=ecuestre)
    form.tipo_de_jya_id.choices = [(t.id, t.tipo) for t in listar_tipos_de_jya()]

    if form.validate_on_submit():
        ecuestre.nombre = form.nombre.data
        ecuestre.fecha_nacimiento = form.fecha_nacimiento.data
        ecuestre.sexo = form.sexo.data
        ecuestre.raza = form.raza.data
        ecuestre.pelaje = form.pelaje.data
        ecuestre.es_compra = form.es_compra.data == "True"
        ecuestre.fecha_ingreso = form.fecha_ingreso.data
        ecuestre.sede = form.sede.data
        ecuestre.tipo_de_jya_id = form.tipo_de_jya_id.data
        guardar_cambios()
        return redirect(url_for("ecuestre.index"))

    return render_template("pages/ecuestre/formulario.html", form=form)


@bp.get("/<int:id>/eliminar/")
def eliminar(id: int):
    eliminar_ecuestre(id)
    flash("Miembro eliminado con exito.", "success")
    return redirect(url_for("ecuestre.index"))
