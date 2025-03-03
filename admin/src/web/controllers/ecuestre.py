from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    current_app,
    send_file,
)
from src.core.ecuestre import (
    crear_ecuestre,
    eliminar_ecuestre,
    eliminar_documento_ecuestre,
    obtener_documento,
    obtener_ecuestre,
    listar_ecuestres,
    listar_documentos,
    listar_tipos_de_jya,
    listar_tipos_de_documentos,
    listar_conductores,
    listar_entrenadores,
    crear_documento,
    guardar_cambios,
)
from src.core.miembro import obtener_miembro
from src.core.forms.ecuestre_form import EcuestreForm
from core.forms.ecuestre_documento_form import (
    SubirArchivoForm,
    EnlaceForm,
    EditarArchivoForm,
)
from os import fstat
from io import BytesIO
import ulid
from src.web.handlers.decoradores import sesion_iniciada_requerida, chequear_permiso
from src.web.handlers.funciones_auxiliares import validar_url, convertir_a_entero

bp = Blueprint("ecuestre", __name__, url_prefix="/ecuestre")


@bp.get("/")
@chequear_permiso("ecuestre_listar")
@sesion_iniciada_requerida
def listar():
    """
    Devuelve la vista de ecuestres en la base de datos
    Los datos se envían paginados, filtrados y ordenados.
    """
    orden = request.args.get("orden", "asc")
    ordenar_por = request.args.get("ordenar_por", "id")
    pagina = convertir_a_entero(request.args.get("pagina", 1))
    cant_por_pagina = int(request.args.get("cant_por_pagina", 6))
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
@chequear_permiso("ecuestre_mostrar")
@sesion_iniciada_requerida
def ver(id: int):
    """
    Devuelve la vista de un ecuestre en particular con el id dado.
    """
    ecuestre = obtener_ecuestre(id)
    return render_template("pages/ecuestre/ver.html", ecuestre=ecuestre)


@bp.route("/crear/", methods=["GET", "POST"])
@chequear_permiso("ecuestre_crear")
@sesion_iniciada_requerida
def crear():
    """
    Devuelve la vista que permite crear un ecuestre.
    """
    form = EcuestreForm()
    form.tipo_de_jya_id.choices = [(t.id, t.tipo) for t in listar_tipos_de_jya()]
    form.conductores.choices = [(-1, "Ninguno")] + [
        (c.id, c.nombre + " " + c.apellido) for c in listar_conductores()
    ]
    form.entrenadores.choices = [(-1, "Ninguno")] + [
        (e.id, e.nombre + " " + e.apellido) for e in listar_entrenadores()
    ]

    if request.method == "POST":
        if form.validate_on_submit():
            nombre = form.nombre.data
            fecha_nacimiento = form.fecha_nacimiento.data
            sexo = form.sexo.data
            raza = form.raza.data
            pelaje = form.pelaje.data
            es_compra = form.es_compra.data
            fecha_ingreso = form.fecha_ingreso.data
            sede = form.sede.data
            tipo_de_jya_id = form.tipo_de_jya_id.data
            conductores = [
                obtener_miembro(conductor)
                for conductor in form.conductores.data
                if conductor != -1
            ]
            entrenadores = [
                obtener_miembro(entrenador)
                for entrenador in form.entrenadores.data
                if entrenador != -1
            ]
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
                conductores,
                entrenadores,
            )
            flash("Ecuestre creado con exito", "exito")
            return redirect(url_for("ecuestre.listar"))
        else:
            flash("Error al crear el ecuestre", "error")

    return render_template(
        "pages/ecuestre/formulario.html", form=form, titulo="Crear ecuestre"
    )


@bp.route("/<int:id>/editar/", methods=["GET", "POST"])
@chequear_permiso("ecuestre_actualizar")
@sesion_iniciada_requerida
def editar(id: int):
    """
    Devuelve la vista que permite editar un ecuestre con el id dado.
    """
    ecuestre = obtener_ecuestre(id)
    form = EcuestreForm(obj=ecuestre)
    form.tipo_de_jya_id.choices = [(t.id, t.tipo) for t in listar_tipos_de_jya()]
    form.entrenadores.choices = [(-1, "Ninguno")] + [
        (e.id, e.nombre + " " + e.apellido) for e in listar_entrenadores()
    ]
    form.conductores.choices = [(-1, "Ninguno")] + [
        (c.id, c.nombre + " " + c.apellido) for c in listar_conductores()
    ]

    if request.method == "POST":
        if form.validate_on_submit():
            ecuestre.nombre = form.nombre.data
            ecuestre.fecha_nacimiento = form.fecha_nacimiento.data
            ecuestre.sexo = form.sexo.data
            ecuestre.raza = form.raza.data
            ecuestre.pelaje = form.pelaje.data
            ecuestre.es_compra = form.es_compra.data
            ecuestre.fecha_ingreso = form.fecha_ingreso.data
            ecuestre.sede = form.sede.data
            ecuestre.tipo_de_jya_id = form.tipo_de_jya_id.data
            ecuestre.conductores = [
                obtener_miembro(conductor)
                for conductor in form.conductores.data
                if conductor != -1
            ]
            ecuestre.entrenadores = [
                obtener_miembro(entrenador)
                for entrenador in form.entrenadores.data
                if entrenador != -1
            ]
            guardar_cambios()
            flash("Ecuestre actualizado con exito", "exito")
            return redirect(url_for("ecuestre.listar"))
        else:
            flash("Error al actualizar el ecuestre", "error")

    form.conductores.data = [c.id for c in ecuestre.conductores]
    form.entrenadores.data = [e.id for e in ecuestre.entrenadores]

    return render_template(
        "pages/ecuestre/formulario.html",
        form=form,
        titulo="Editar ecuestre #" + str(id),
    )


@bp.get("/<int:id>/eliminar/")
@chequear_permiso("ecuestre_eliminar")
@sesion_iniciada_requerida
def eliminar(id: int):
    """
    Elimina un ecuestre con el id dado.
    """
    try:
        eliminar_ecuestre(id)
        flash("Ecuestre eliminado con exito", "exito")
    except ValueError as e:
        flash(str(e), "error")
    return redirect(url_for("ecuestre.listar"))


@bp.get("/<int:id>/documentos/")
@chequear_permiso("ecuestre_mostrar")
@sesion_iniciada_requerida
def documentos(id: int):
    """
    Devuelve la vista de documentos de un ecuestre en particular con el id dado.
    """
    ecuestre = obtener_ecuestre(id)
    orden = request.args.get("orden", "asc")
    ordenar_por = request.args.get("ordenar_por", "id")
    pagina = convertir_a_entero(request.args.get("pagina", 1))
    cant_por_pagina = int(request.args.get("cant_por_pagina", 6))
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


@bp.route("/<int:id>/documentos/subir_archivo/", methods=["GET", "POST"])
@chequear_permiso("ecuestre_crear")
@sesion_iniciada_requerida
def subir_archivo(id: int):
    """
    Devuelve la vista que permite subir un archivo a un ecuestre con el id dado.
    """
    ecuestre = obtener_ecuestre(id)
    form = SubirArchivoForm()
    form.tipo_de_documento_id.choices = [
        (t.id, t.tipo) for t in listar_tipos_de_documentos()
    ]

    if request.method == "POST":
        if form.validate_on_submit():
            nombre = form.nombre.data
            tipo = form.tipo_de_documento_id.data
            ecuestre_id = id
            archivo = request.files["archivo"]
            client = current_app.storage.client
            size = fstat(archivo.fileno()).st_size
            url = f"ecuestre/{ulid.new()}-{archivo.filename}"

            client.put_object(
                "grupo17",
                url,
                archivo,
                size,
                content_type=archivo.content_type,
            )

            crear_documento(nombre, tipo, url, ecuestre_id, archivo_externo=False)

            flash("Documento subido con exito", "exito")
            return redirect(url_for("ecuestre.documentos", id=id))
        else:
            flash("Error al subir el documento", "error")

    return render_template(
        "pages/ecuestre/formulario_documento.html",
        form=form,
        ecuestre=ecuestre,
        titulo="Subir archivo",
        subir_archivo=True,
    )


@bp.route("/<int:id>/documentos/subir_enlace/", methods=["GET", "POST"])
@chequear_permiso("ecuestre_crear")
@sesion_iniciada_requerida
def subir_enlace(id: int):
    """
    Devuelve la vista que permite subir un enlace a un ecuestre con el id dado.
    """
    ecuestre = obtener_ecuestre(id)
    form = EnlaceForm()
    form.tipo_de_documento_id.choices = [
        (t.id, t.tipo) for t in listar_tipos_de_documentos()
    ]

    if request.method == "POST":
        if form.validate_on_submit():
            nombre = form.nombre.data
            tipo = form.tipo_de_documento_id.data
            ecuestre_id = id
            url = validar_url(form.url.data)

            crear_documento(nombre, tipo, url, ecuestre_id, archivo_externo=True)

            flash("Documento subido con exito", "exito")
            return redirect(url_for("ecuestre.documentos", id=id))
        else:
            flash("Error al subir el documento", "error")

    return render_template(
        "pages/ecuestre/formulario_documento.html",
        form=form,
        ecuestre=ecuestre,
        titulo="Subir enlace",
        subir_enlace=True,
    )


@bp.get("/<int:id>/documentos/<int:documento_id>/eliminar/")
@chequear_permiso("ecuestre_eliminar")
@sesion_iniciada_requerida
def eliminar_documento(id: int, documento_id: int):
    """
    Elimina un documento con el id dado.
    """
    eliminar_documento_ecuestre(documento_id)
    flash("Documento eliminado con exito", "exito")
    return redirect(url_for("ecuestre.documentos", id=id))


@bp.get("/<int:id>/documentos/<int:documento_id>/descargar/")
@chequear_permiso("ecuestre_mostrar")
@sesion_iniciada_requerida
def descargar_documento(id: int, documento_id: int):
    """
    Descarga un documento con el id dado.
    """
    documento = obtener_documento(documento_id)
    client = current_app.storage.client
    archivo = client.get_object("grupo17", documento.url)

    # Convertir el archivo a un objeto BytesIO
    archivo_bytes = BytesIO(archivo.read())

    # Obtener la extensión del archivo
    extension = f".{documento.url.split('.')[-1]}" if "." in documento.url else ""

    # Enviar el archivo al cliente
    return send_file(
        archivo_bytes,
        as_attachment=True,
        download_name=f"{documento.nombre}{extension}",  # Nombre del archivo para la descarga
    )


@bp.get("/<int:id>/documentos/<int:documento_id>/ir/")
@chequear_permiso("ecuestre_mostrar")
@sesion_iniciada_requerida
def ir_documento(id: int, documento_id: int):
    """
    Redirige a la URL del documento con el id dado.
    """
    documento = obtener_documento(documento_id)
    return redirect(documento.url)


@bp.route("/<int:id>/documentos/<int:documento_id>/editar/", methods=["GET", "POST"])
@chequear_permiso("ecuestre_actualizar")
@sesion_iniciada_requerida
def editar_documento(id: int, documento_id: int):
    """
    Devuelve la vista que permite editar un documento con el id dado.
    """
    documento = obtener_documento(documento_id)
    if documento.archivo_externo:
        form = EnlaceForm(obj=documento)
    else:
        form = EditarArchivoForm(obj=documento)
    form.tipo_de_documento_id.choices = [
        (t.id, t.tipo) for t in listar_tipos_de_documentos()
    ]

    if request.method == "POST":
        if form.validate_on_submit():
            documento.nombre = form.nombre.data
            documento.tipo_de_documento_id = form.tipo_de_documento_id.data
            if documento.archivo_externo:
                documento.url = validar_url(form.url.data)
            guardar_cambios()
            flash("Documento actualizado con exito", "exito")
            return redirect(url_for("ecuestre.documentos", id=id))
        else:
            flash("Error al actualizar el documento", "error")

    return render_template(
        "pages/ecuestre/formulario_documento.html",
        form=form,
        ecuestre=documento.ecuestre,
        titulo=f"Editar documento #{documento_id}",
        subir_enlace=documento.archivo_externo,
    )
