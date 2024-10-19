from flask import Blueprint, render_template, request, redirect, url_for, flash
from src.core.ecuestre import (
    crear_ecuestre,
    eliminar_ecuestre,
    obtener_ecuestre,
    listar_ecuestres,
    listar_documentos,
    listar_tipos_de_jya,
    listar_tipos_de_documentos,
    crear_documento,
    guardar_cambios,
)
from src.core.ecuestre.ecuestre_form import EcuestreForm
from src.core.ecuestre.documento_form import DocumentoForm


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

    if request.method == "POST":
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
            flash("Ecuestre creado con exito", "exito")
            return redirect(url_for("ecuestre.index"))
        else:
            flash("Error al crear el ecuestre", "error")

    return render_template(
        "pages/ecuestre/formulario.html", form=form, titulo="Crear ecuestre"
    )


@bp.route("/<int:id>/editar/", methods=["GET", "POST"])
def editar(id: int):
    ecuestre = obtener_ecuestre(id)
    form = EcuestreForm(obj=ecuestre)
    form.tipo_de_jya_id.choices = [(t.id, t.tipo) for t in listar_tipos_de_jya()]

    if request.method == "POST":
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
            flash("Ecuestre actualizado con exito", "exito")
            return redirect(url_for("ecuestre.index"))
        else:
            flash("Error al actualizar el ecuestre", "error")

    return render_template(
        "pages/ecuestre/formulario.html",
        form=form,
        titulo="Editar ecuestre #" + str(id),
    )


@bp.get("/<int:id>/eliminar/")
def eliminar(id: int):
    eliminar_ecuestre(id)
    flash("Ecuestre eliminado con exito", "exito")
    return redirect(url_for("ecuestre.index"))


@bp.get("/<int:id>/documentos/")
def documentos(id: int):
    ecuestre = obtener_ecuestre(id)
    orden = request.args.get("orden", "asc")
    ordenar_por = request.args.get("ordenar_por", "id")
    pagina = int(request.args.get("pagina", 1))
    cant_por_pagina = int(request.args.get("cant_por_pagina", 10))
    nombre_filtro = request.args.get("nombre", "")
    tipo_filtro = request.args.get("tipo", "")

    documentos, cant_resultados = listar_documentos(
        ecuestre.id,
        nombre_filtro,
        tipo_filtro,
        ordenar_por,
        orden,
        pagina,
        cant_por_pagina,
    )

    tipos_documento = listar_tipos_de_documentos()

    cant_paginas = cant_resultados // cant_por_pagina
    if cant_resultados % cant_por_pagina != 0:
        cant_paginas += 1

    return render_template(
        "pages/ecuestre/documentos.html",
        ecuestre=ecuestre,
        documentos=documentos,
        cant_resultados=cant_resultados,
        cant_paginas=cant_paginas,
        pagina=pagina,
        orden=orden,
        ordenar_por=ordenar_por,
        nombre_filtro=nombre_filtro,
        tipo_filtro=tipo_filtro,
        tipos_documento=tipos_documento,
    )


@bp.route("/<int:id>/documentos/subir/", methods=["GET", "POST"])
def subir_documento(id: int):
    ecuestre = obtener_ecuestre(id)
    form = DocumentoForm()
    form.tipo.choices = [(t.value, t.name) for t in listar_tipos_de_documentos()]

    if request.method == "POST":
        if form.validate_on_submit():
            nombre = form.nombre.data
            tipo = form.tipo.data
            url = form.url.data
            ecuestre_id = id
            crear_documento(nombre, tipo, url, ecuestre_id)
            flash("Documento subido con exito", "exito")
            return redirect(url_for("ecuestre.documentos", id=id))
        else:
            flash("Error al subir el documento", "error")

    return render_template(
        "pages/ecuestre/subir_documento.html", form=form, ecuestre=ecuestre
    )
