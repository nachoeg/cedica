import ulid
from io import BytesIO
from os import fstat
from flask import render_template, request, redirect, url_for, send_file, flash
from flask import Blueprint
from flask import current_app
from src.core.forms.forms_documentos_jya import SubirArchivoForm
from src.core.forms.forms_documentos_jya import EnlaceForm
from src.core.jinetes_y_amazonas import (
    listar_j_y_a,
    crear_j_o_a,
    cargar_informacion_salud,
    cargar_informacion_economica,
    cargar_informacion_escuela,
    cargar_informacion_institucional,
    eliminar_jya,
    encontrar_jya,
    cargar_archivo,
    encontrar_archivo,
    listar_documentos,
    listar_tipos_de_documentos,
    listar_diagnosticos,
    listar_profesores,
    listar_conductores,
    listar_auxiliares_pista,
    listar_caballos,
    listar_dias,
    eliminar_documento_j_y_a,
    guardar_cambios,
    cargar_id_diagnostico_otro,
    obtener_dia,
    crear_familiar,
    encontrar_familiar,
    listar_familiares,
    obtener_tipo_discapacidad,
    listar_tipos_de_discapacidad
)
from core.forms.forms_jinetes import (
    NuevoJYAForm,
    InfoSaludJYAForm,
    InfoEconomicaJYAForm,
    InfoEscolaridadJYAForm,
    InfoInstitucionalJYAForm,
    FamiliarForm
)
from src.web.handlers.decoradores import (
    sesion_iniciada_requerida, chequear_permiso
    )
from src.web.handlers.funciones_auxiliares import (
    validar_url, convertir_a_entero, calcular_edad)


bp = Blueprint("jinetes_y_amazonas", __name__,
               url_prefix="/jinetes_y_amazonas")


@bp.get("/")
@chequear_permiso("jya_listar")
@sesion_iniciada_requerida
def listar():
    """
    Controlador que muestra el listado de jinetes y amazonas del sistema.
    """
    orden = request.args.get("orden", "asc")
    ordenar_por = request.args.get("ordenar_por", "id")
    pagina = convertir_a_entero(request.args.get("pagina", 1))
    cant_por_pag = int(request.args.get("por_pag", 6))
    nombre_filtro = request.args.get("nombre", "")
    apellido_filtro = request.args.get("apellido", "")
    dni_filtro = request.args.get("dni", "")
    profesionales_a_cargo = request.args.get("profesionales_a_cargo", "")

    jinetes, cant_resultados = listar_j_y_a(
        nombre_filtro,
        apellido_filtro,
        dni_filtro,
        profesionales_a_cargo,
        ordenar_por,
        orden,
        pagina,
        cant_por_pag,
    )

    cant_paginas = cant_resultados // cant_por_pag
    if cant_resultados % cant_por_pag != 0:
        cant_paginas += 1

    return render_template(
        "pages/jinetes_y_amazonas/listar.html",
        jinetes=jinetes,
        cant_resultados=cant_resultados,
        cant_paginas=cant_paginas,
        pagina=pagina,
        orden=orden,
        ordenar_por=ordenar_por,
        nombre_filtro=nombre_filtro,
        apellido_filtro=apellido_filtro,
        dni_filtro=dni_filtro,
        profesionales_a_cargo=profesionales_a_cargo,
    )


@bp.route("/nuevo_joa", methods=["GET", "POST"])
@chequear_permiso("jya_crear")
@sesion_iniciada_requerida
def nuevo_j_y_a():
    """
    Controlador que muestra el formulario de alta
    de un jinete o amazona o guarda los datos ingresados en él.
    """
    form = NuevoJYAForm()
    form.submit.label.text = "Continuar"
    if form.validate_on_submit():

        nombre = form.nombre.data
        apellido = form.apellido.data
        dni = form.dni.data
        fecha_nacimiento = form.fecha_nacimiento.data
        provincia_nacimiento = form.provincia_nacimiento.data
        localidad_nacimiento = form.localidad_nacimiento.data
        domicilio_actual = form.domicilio_actual.data
        telefono_actual = form.telefono_actual.data
        contacto_emer_nombre = form.contacto_emer_nombre.data
        contacto_emer_telefono = form.contacto_emer_telefono.data
        becado = form.becado.data

        if becado:
            porcentaje_beca = form.porcentaje_beca.data
        else:
            becado = False
            porcentaje_beca = 0

        jya_nuevo = crear_j_o_a(
            nombre,
            apellido,
            dni,
            fecha_nacimiento,
            provincia_nacimiento,
            localidad_nacimiento,
            domicilio_actual,
            telefono_actual,
            contacto_emer_nombre,
            contacto_emer_telefono,
            becado,
            porcentaje_beca
        )

        flash("Nuevo J&A creado. \
              Continúe con la carga de información", "exito")
        return redirect(
            url_for("jinetes_y_amazonas.cargar_info_salud", id=jya_nuevo.id)
        )

    return render_template(
        "pages/jinetes_y_amazonas/nuevo_j_y_a.html",
        form=form,
        titulo="Nuevo jinete/amazona",
    )


@bp.route("/cargar_info_salud/<int:id>", methods=["GET", "POST"])
@chequear_permiso("jya_crear")
@sesion_iniciada_requerida
def cargar_info_salud(id: int):
    """
    Controlador que muestra muestra el formulario de alta
    de la información de salud del jinete o amazona
    o guarda los datos asociados a él.
    """
    jya = encontrar_jya(id)
    form = InfoSaludJYAForm()
    form.diagnostico.choices = [
        (diagnostico.id, diagnostico.nombre)
        for diagnostico in listar_diagnosticos()
    ]
    id_otro_diagnostico = cargar_id_diagnostico_otro()
    form.tipo_discapacidad.choices = [
        (tipo.id, tipo.nombre)
        for tipo in listar_tipos_de_discapacidad()]

    form.submit.label.text = "Continuar"

    if form.validate_on_submit():
        certificado_discapacidad = form.certificado_discapacidad.data

        if certificado_discapacidad:
            diagnostico_id = form.diagnostico.data
            if diagnostico_id == id_otro_diagnostico:
                diagnostico_otro = form.diagnostico_otro.data
            else:
                diagnostico_otro = None
            tipo_discapacidad = []
        else:
            diagnostico_id = None
            diagnostico_otro = None
            tipo_discapacidad = [
                obtener_tipo_discapacidad(tipo)
                for tipo in form.tipo_discapacidad
            ]
        cargar_informacion_salud(
            id,
            certificado_discapacidad,
            diagnostico_id,
            diagnostico_otro,
            tipo_discapacidad,
        )
        flash("Información de salud guardada. Continúe con la carga.", "exito")

        return redirect(url_for("jinetes_y_amazonas.cargar_info_econ", id=id))

    return render_template(
        "pages/jinetes_y_amazonas/nuevo_j_y_a_salud.html",
        form=form,
        jya=jya,
        titulo="Nuevo jinete/amazona",
        id_otro_diagnostico=id_otro_diagnostico
    )


@bp.route("/cargar_info_econ/<int:id>", methods=["GET", "POST"])
@chequear_permiso("jya_crear")
@sesion_iniciada_requerida
def cargar_info_econ(id: int):
    """
    Controlador que muestra el formulario de carga
    de la información económica del jinete o amazona,
    o guarda los datos ingrsados en él.
    """
    jya = encontrar_jya(id)
    form = InfoEconomicaJYAForm()
    form.submit.label.text = "Continuar"

    if form.validate_on_submit():
        asignacion_familiar = form.asignacion_familiar.data

        if asignacion_familiar:
            tipo_asignacion_familiar = form.tipo_asignacion_familiar.data
        else:
            asignacion_familiar = False
            tipo_asignacion_familiar = None

        beneficiario_pension = form.beneficiario_pension.data

        if beneficiario_pension:
            tipo_pension = form.tipo_pension.data
        else:
            beneficiario_pension = False
            tipo_pension = None

        obra_social = form.obra_social.data
        num_afiliado = form.num_afiliado.data
        posee_curatela = form.posee_curatela.data
        observaciones_obra_social = form.observaciones_obra_social.data

        cargar_informacion_economica(
            id,
            asignacion_familiar,
            tipo_asignacion_familiar,
            beneficiario_pension,
            tipo_pension,
            obra_social,
            num_afiliado,
            posee_curatela,
            observaciones_obra_social,
        )
        flash("Información económica guardada. Continúe con la carga", "exito")
        return redirect(url_for("jinetes_y_amazonas.cargar_info_esc", id=id))
    return render_template(
        "pages/jinetes_y_amazonas/nuevo_j_y_a_econ.html",
        form=form,
        jya=jya,
        titulo="Nuevo jinete/amazona",
    )


@bp.route("/cargar_info_esc/<int:id>", methods=["GET", "POST"])
@chequear_permiso("jya_crear")
@sesion_iniciada_requerida
def cargar_info_esc(id: int):
    """
    Controlador que muestra el formulario
    para la carga de información de escolaridad del jinete o amazona,
    o guarda los datos cargados en él.
    """
    jya = encontrar_jya(id)
    form = InfoEscolaridadJYAForm()
    form.submit.label.text = "Continuar"

    if form.validate_on_submit():
        nombre_escuela = form.nombre_escuela.data
        direccion_escuela = form.direccion_escuela.data
        telefono_escuela = form.telefono_escuela.data
        grado_escuela = form.grado_escuela.data
        observaciones_escuela = form.observaciones_escuela.data
        profesionales_a_cargo = form.profesionales_a_cargo.data
        cargar_informacion_escuela(
            id,
            nombre_escuela,
            direccion_escuela,
            telefono_escuela,
            grado_escuela,
            observaciones_escuela,
            profesionales_a_cargo,
        )
        flash("Informacion de escolaridad guardada.\
               Continúe con la carga.", "exito")
        return redirect(url_for("jinetes_y_amazonas.cargar_info_inst", id=id))
    return render_template(
        "pages/jinetes_y_amazonas/nuevo_j_y_a_esc.html",
        form=form,
        jya=jya,
        titulo="Nuevo jinete/amazona",
    )


@bp.route("/cargar_info_inst/<int:id>", methods=["GET", "POST"])
@chequear_permiso("jya_crear")
@sesion_iniciada_requerida
def cargar_info_inst(id: int):
    """
    Controlador que muestra el formulario
    para la carga de información institucional del jinete o amazona,
    o guarda los datos cargados en él.
    """
    jya = encontrar_jya(id)
    form = InfoInstitucionalJYAForm()
    form.submit.label.text = "Finalizar"

    form.profesor_id.choices = [
        (profesor.id, profesor.nombre + " " + profesor.apellido)
        for profesor in listar_profesores()
    ]
    form.conductor_caballo_id.choices = [
        (conductor.id, conductor.nombre + " " + conductor.apellido)
        for conductor in listar_conductores()
    ]
    form.caballo_id.choices = [
        (caballo.id, caballo.nombre)
        for caballo in listar_caballos()
    ]
    form.auxiliar_pista_id.choices = [
        (auxiliar.id, auxiliar.nombre + " " + auxiliar.apellido)
        for auxiliar in listar_auxiliares_pista()
    ]
    form.dias.choices = [
        (dia.id, dia.nombre)
        for dia in listar_dias()
    ]
    if form.validate_on_submit():
        propuesta_de_trabajo = form.propuesta_trabajo.data
        condicion = form.condicion.data
        sede = form.sede.data
        profesor_id = form.profesor_id.data
        conductor_caballo_id = form.profesor_id.data
        caballo_id = form.caballo_id.data
        auxiliar_pista_id = form.auxiliar_pista_id.data
        dias = [
                obtener_dia(dia)
                for dia in form.dias.data
            ]
        cargar_informacion_institucional(
            id,
            propuesta_de_trabajo,
            condicion,
            sede,
            dias,
            profesor_id,
            conductor_caballo_id,
            caballo_id,
            auxiliar_pista_id,
        )

        flash("Información institucional guardada.\
              Continúe con la carga.", "exito")
        return redirect(url_for("jinetes_y_amazonas.listar"))

    return render_template(
        "pages/jinetes_y_amazonas/nuevo_j_y_a_inst.html",
        form=form,
        jya=jya,
        titulo="Nuevo jinete/amazona",
    )


@bp.get("/<int:id>/")
@chequear_permiso("jya_mostrar")
@sesion_iniciada_requerida
def ver(id: int):
    """
    Controlador que permite visualizar la información de un jinete o amazona.
    """
    jya = encontrar_jya(id)

    return render_template("pages/jinetes_y_amazonas/ver_jya.html",
                           jya=jya,
                           edad=calcular_edad(jya.fecha_nacimiento))


@bp.get("/<int:id>/salud")
@chequear_permiso("jya_mostrar")
@sesion_iniciada_requerida
def ver_salud(id: int):
    """
    Controlador que permite visualizar la información de un jinete o amazona.
    """
    jya = encontrar_jya(id)

    return render_template("pages/jinetes_y_amazonas/ver_salud.html",
                           jya=jya)


@bp.get("/<int:id>/economica")
@chequear_permiso("jya_mostrar")
@sesion_iniciada_requerida
def ver_economica(id: int):
    """
    Controlador que permite visualizar la información de un jinete o amazona.
    """
    jya = encontrar_jya(id)

    return render_template("pages/jinetes_y_amazonas/ver_economica.html",
                           jya=jya)


@bp.get("/<int:id>/escolaridad")
@chequear_permiso("jya_mostrar")
@sesion_iniciada_requerida
def ver_escolaridad(id: int):
    """
    Controlador que permite visualizar la información de un jinete o amazona.
    """
    jya = encontrar_jya(id)

    return render_template("pages/jinetes_y_amazonas/ver_escolaridad.html",
                           jya=jya)


@bp.get("/<int:id>/institucional")
@chequear_permiso("jya_mostrar")
@sesion_iniciada_requerida
def ver_institucional(id: int):
    """
    Controlador que permite visualizar la información de un jinete o amazona.
    """
    jya = encontrar_jya(id)

    return render_template("pages/jinetes_y_amazonas/ver_institucional.html",
                           jya=jya)


@bp.get("/<int:id>/eliminar/")
@chequear_permiso("jya_eliminar")
@sesion_iniciada_requerida
def eliminar(id: int):
    """
    Controlador que elimina un jinete o amazona
    y redirige al listado de jinetes y amazonas
    """
    eliminar_jya(id)

    flash("J&A eliminado con éxito.", "exito")
    return redirect(url_for("jinetes_y_amazonas.listar"))


@bp.route("/<int:id>/subir_archivo/", methods=["GET", "POST"])
@chequear_permiso("jya_crear")
@sesion_iniciada_requerida
def subir_archivo(id: int):
    """
    Controlador que muestra el formulario
    para el alta de un archivo en el sistema.
    """

    form = SubirArchivoForm()

    if request.method == "POST":
        if form.validate_on_submit():
            titulo = form.titulo.data
            jya_id = id
            tipo_archivo = form.tipo_de_documento_id.data
            archivo = request.files["archivo"]
            cliente = current_app.storage.client
            tamaño = fstat(archivo.fileno()).st_size
            url = f"jinetes_y_amazonas/{ulid.new()}-{archivo.filename}"
            cliente.put_object(
                "grupo17", url, archivo,
                tamaño, content_type=archivo.content_type
            )

            cargar_archivo(jya_id, titulo,
                           tipo_archivo, url, archivo_externo=False)
            flash("Archivo subido con éxito", "exito")

            return redirect(url_for("jinetes_y_amazonas.ver_archivos", id=id))
        else:
            flash("Error al subir el archivo", "error")
    return render_template(
        "pages/jinetes_y_amazonas/crear_documento.html",
        form=form,
        jya=id,
        titulo="Subir archivo",
        subir_archivo=True,
    )


@bp.route("/<int:id>/subir_enlace/", methods=["GET", "POST"])
@chequear_permiso("jya_crear")
@sesion_iniciada_requerida
def subir_enlace(id: int):
    """
    Controlador que muestra el formulario para el alta
    de un archivo externo en el sistema (enlace a un archivo externo).
    """

    form = EnlaceForm()

    if request.method == "POST":
        if form.validate_on_submit():
            titulo = form.titulo.data
            jya_id = id
            url = validar_url(form.url.data)
            tipo_archivo = form.tipo_de_documento_id.data
            cargar_archivo(jya_id,
                           titulo,
                           tipo_archivo,
                           url,
                           archivo_externo=True)

            flash("Enlace a documento subido con exito", "exito")
            return redirect(url_for("jinetes_y_amazonas.ver_archivos", id=id))
        else:
            flash("Error al subir el documento", "error")

    return render_template(
        "pages/jinetes_y_amazonas/crear_documento.html",
        form=form,
        jya=id,
        titulo="Subir enlace",
        subir_enlace=True,
    )


@bp.get("/<int:id>/archivos")
@chequear_permiso("jya_mostrar")
@sesion_iniciada_requerida
def ver_archivos(id: int):
    """
    Controlador que devuelve el listado
    de archivos asociados a un jinete o amazona.
    """
    jya = encontrar_jya(id)
    orden = request.args.get("orden", "asc")
    ordenar_por = request.args.get("ordenar_por", "id")
    pagina = convertir_a_entero(request.args.get("pagina", 1))
    cant_por_pagina = int(request.args.get("cant_por_pagina", 6))
    nombre_filtro = request.args.get("nombre", "")
    tipo_filtro = request.args.get("tipo", "")

    documentos, cant_resultados = listar_documentos(
        jya.id,
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
        "pages/jinetes_y_amazonas/listar_documentos.html",
        jya=jya,
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


@bp.route("/editar_archivo/<int:id>", methods=["GET", "POST"])
@chequear_permiso("jya_actualizar")
@sesion_iniciada_requerida
def editar_archivo(id: int):
    """
    Controlador que muestra el formulario
    para la edición de un archivo o enlace.
    """
    archivo = encontrar_archivo(id)
    if archivo.externo:
        form = EnlaceForm(obj=archivo)
    else:
        form = SubirArchivoForm(obj=archivo)

    if request.method == "GET":
        form.tipo_de_documento_id.data = archivo.tipo_archivo.name

    if request.method == "POST":
        if form.validate_on_submit():
            archivo.titulo = form.titulo.data
            archivo.url = validar_url(form.url.data)
            archivo.tipo_archivo = form.tipo_de_documento_id.data

            guardar_cambios()
            flash("El documento ha sido editado con éxito", "exito")
            return redirect(url_for("jinetes_y_amazonas.ver_archivos",
                                    id=archivo.jya_id))

        else:
            flash("Error al editar el documento", "error")

    return render_template(
        "pages/jinetes_y_amazonas/crear_documento.html",
        form=form,
        jya=archivo.jya_id,
        titulo="Editar documento",
        subir_enlace=archivo.externo,
    )


@bp.get("/descargar_archivo/<int:archivo_id>")
@chequear_permiso("jya_mostrar")
@sesion_iniciada_requerida
def descargar_archivo(archivo_id: int):
    """
    Controlador que permite la descarga de un archivo dado su id.
    """
    documento = encontrar_archivo(archivo_id)
    cliente = current_app.storage.client
    archivo = cliente.get_object("grupo17", documento.url)
    archivo_bytes = BytesIO(archivo.read())
    extension = (
        f".{documento.url.split('.')[-1]}"if "." in documento.url else "")

    return send_file(
        archivo_bytes,
        as_attachment=True,
        download_name=f"{documento.titulo}{extension}",
    )


@bp.get("/documentos/<int:documento_id>/ir/")
@chequear_permiso("jya_mostrar")
@sesion_iniciada_requerida
def ir_documento(documento_id: int):
    """
    Redirige a la URL del documento con el id dado.
    """
    documento = encontrar_archivo(documento_id)
    return redirect(documento.url)


@bp.get("/eliminar_archivo/<int:id>")
@chequear_permiso("jya_eliminar")
@sesion_iniciada_requerida
def eliminar_documento(id: int):
    """
    Controlador que permite la eliminación de un documento y
    redirige a la vista de listado de archivos.
    """
    doc = eliminar_documento_j_y_a(id)
    flash("Documento eliminado con éxito")

    return redirect(url_for("jinetes_y_amazonas.ver_archivos", id=doc.jya_id))


@bp.route("/<int:id>/editar", methods=["GET", "POST"])
@chequear_permiso("jya_actualizar")
@sesion_iniciada_requerida
def editar_j_y_a(id: int):
    """
    Controlador que muestra permite editar
    la información general del jinete o amazona.
    """
    jya = encontrar_jya(id)
    form = NuevoJYAForm(obj=jya)
    form.submit.label.text = "Guardar"
    if request.method == "GET":
        form.edad.data = calcular_edad(form.fecha_nacimiento.data)
    if request.method == "POST":
        if form.validate_on_submit():
            jya.nombre = form.nombre.data
            jya.apellido = form.apellido.data
            jya.dni = form.dni.data
            jya.fecha_nacimiento = form.fecha_nacimiento.data
            jya.provincia_nacimiento = form.provincia_nacimiento.data
            jya.localidad_nacimiento = form.localidad_nacimiento.data
            jya.domicilio_actual = form.domicilio_actual.data
            jya.telefono_actual = form.telefono_actual.data
            jya.contacto_emer_nombre = form.contacto_emer_nombre.data
            jya.contacto_emer_telefono = form.contacto_emer_telefono.data
            jya.becado = form.becado.data

            if jya.becado:
                jya.porcentaje_beca = form.porcentaje_beca.data
            else:
                jya.porcentaje_beca = 0

            guardar_cambios()
            flash("Jinete/Amazona: Información actualizada con éxito", "exito")
            return redirect(url_for("jinetes_y_amazonas.ver", id=id))
        else:
            flash("Error al actualizar jinete/amazona", "error")

    return render_template(
        "pages/jinetes_y_amazonas/nuevo_j_y_a.html",
        form=form,
        jya=jya,
        titulo="Editar J/A " + str(jya.nombre) +
        " " + str(jya.apellido)
    )


@bp.route("/editar_info_salud/<int:id>", methods=["GET", "POST"])
@chequear_permiso("jya_actualizar")
@sesion_iniciada_requerida
def editar_info_salud(id: int):
    """
    Controlador que muestra permite editar
    la información de salud del jinete o amazona.
    """
    jya = encontrar_jya(id)
    form = InfoSaludJYAForm(obj=jya)
    form.diagnostico.choices = [
        (diagnostico.id, diagnostico.nombre)
        for diagnostico in listar_diagnosticos()
    ]
    id_otro_diagnostico = cargar_id_diagnostico_otro()

    form.tipo_discapacidad.choices = [
        (tipo.id, tipo.nombre)
        for tipo in listar_tipos_de_discapacidad()]

    form.submit.label.text = "Guardar"

    if request.method == "GET":
        if jya.diagnostico is not None:
            form.diagnostico.data = jya.diagnostico.id

        form.tipo_discapacidad.data = [
            tipo.id for tipo in jya.tipo_discapacidad]

    if request.method == "POST":
        if form.validate_on_submit():
            jya.certificado_discapacidad = form.certificado_discapacidad.data
            if jya.certificado_discapacidad:
                jya.diagnostico_id = form.diagnostico.data
                if jya.diagnostico_id == id_otro_diagnostico:
                    jya.diagnostico_otro = form.diagnostico_otro.data
                else:
                    jya.diagnostico_otro = None
                jya.tipo_discapacidad = []
            else:
                jya.diagnostico_id = None
                jya.diagnostico_otro = None
                jya.tipo_discapacidad = [
                    obtener_tipo_discapacidad(tipo)
                    for tipo in form.tipo_discapacidad.data]
            guardar_cambios()

            flash("Jinete/Amazona: Información actualizada con éxito", "exito")
            return redirect(url_for("jinetes_y_amazonas.ver", id=id))
        else:
            flash("Error al actualizar jinete/amazona", "error")

    return render_template(
        "pages/jinetes_y_amazonas/nuevo_j_y_a_salud.html",
        form=form,
        jya=jya,
        titulo="Editar información de salud - J/A "
        + str(jya.nombre)
        + " "
        + str(jya.apellido),
        id_otro_diagnostico=id_otro_diagnostico
    )


@bp.route("/editar_info_econ/<int:id>", methods=["GET", "POST"])
@chequear_permiso("jya_actualizar")
@sesion_iniciada_requerida
def editar_info_econ(id: int):
    """
    Controlador que muestra permite editar
    la información economica del jinete o amazona.
    """
    jya = encontrar_jya(id)
    form = InfoEconomicaJYAForm(obj=jya)
    form.submit.label.text = "Guardar"

    if request.method == "POST":
        if form.validate_on_submit():
            jya.asignacion_familiar = form.asignacion_familiar.data

            if jya.asignacion_familiar:
                jya.tipo_asignacion_familiar = form.tipo_asignacion_familiar.data
            else:
                jya.asignacion_familiar = False
                jya.tipo_asignacion_familiar = None
            jya.beneficiario_pension = form.beneficiario_pension.data

            if jya.beneficiario_pension:
                jya.tipo_pension = form.tipo_pension.data
            else:
                jya.beneficiario_pension = False
                jya.tipo_pension = None

            jya.obra_social = form.obra_social.data
            jya.num_afiliado = form.num_afiliado.data
            jya.posee_curatela = form.posee_curatela.data
            jya.observaciones_obra_social = form.observaciones_obra_social.data

            guardar_cambios()
            flash("Jinete/Amazona: Información actualizada con éxito", "exito")
            return redirect(url_for("jinetes_y_amazonas.ver", id=id))
        else:
            flash("Error al actualizar jinete/amazona", "error")
    return render_template(
        "pages/jinetes_y_amazonas/nuevo_j_y_a_econ.html",
        form=form,
        jya=jya,
        titulo="Editar información económica - J/A "
        + str(jya.nombre)
        + " "
        + str(jya.apellido),
    )


@bp.route("/editar_info_esc/<int:id>", methods=["GET", "POST"])
@chequear_permiso("jya_actualizar")
@sesion_iniciada_requerida
def editar_info_esc(id: int):
    """
    Controlador que muestra permite editar
    la información sobre escolaridad del jinete o amazona.
    """
    jya = encontrar_jya(id)
    form = InfoEscolaridadJYAForm(obj=jya)
    form.submit.label.text = "Guardar"

    if request.method == "POST":
        if form.validate_on_submit():
            jya.nombre_escuela = form.nombre_escuela.data
            jya.direccion_escuela = form.direccion_escuela.data
            jya.telefono_escuela = form.telefono_escuela.data
            jya.grado_escuela = form.grado_escuela.data
            jya.observaciones_escuela = form.observaciones_escuela.data
            jya.profesionales_a_cargo = form.profesionales_a_cargo.data
            guardar_cambios()

            flash("Jinete/Amazona: Información actualizada con éxito", "exito")
            return redirect(url_for("jinetes_y_amazonas.ver", id=id))
        else:
            flash("Error al actualizar jinete/amazona", "error")

    return render_template(
        "pages/jinetes_y_amazonas/nuevo_j_y_a_esc.html",
        form=form,
        jya=jya,
        titulo="Editar información sobre escolaridad - J/A "
        + str(jya.nombre)
        + " "
        + str(jya.apellido),
    )


@bp.route("/editar_info_inst/<int:id>", methods=["GET", "POST"])
@chequear_permiso("jya_actualizar")
@sesion_iniciada_requerida
def editar_info_inst(id: int):
    """
    Controlador que muestra permite editar
    la información institucional relacionada al jinete o amazona.
    """
    jya = encontrar_jya(id)
    form = InfoInstitucionalJYAForm(obj=jya)

    form.profesor_id.choices = [
        (profesor.id, profesor.nombre + " " + profesor.apellido)
        for profesor in listar_profesores()
    ]
    form.conductor_caballo_id.choices = [
        (conductor.id, conductor.nombre + " " + conductor.apellido)
        for conductor in listar_conductores()
    ]
    form.caballo_id.choices = [
        (caballo.id, caballo.nombre)
        for caballo in listar_caballos()
    ]
    form.auxiliar_pista_id.choices = [
        (auxiliar.id, auxiliar.nombre + " " + auxiliar.apellido)
        for auxiliar in listar_auxiliares_pista()
    ]

    form.dias.choices = [
        (dia.id, dia.nombre)
        for dia in listar_dias()
    ]

    form.submit.label.text = "Guardar"

    if request.method == "GET":
        if jya.propuesta_trabajo is not None:
            form.propuesta_trabajo.data = jya.propuesta_trabajo.name

        if jya.condicion is not None:
            form.condicion.data = jya.condicion.name

        if jya.profesor is not None:
            form.profesor_id.data = jya.profesor.id

        if jya.conductor_caballo is not None:
            form.conductor_caballo_id.data = jya.conductor_caballo.id

        if jya.caballo is not None:
            form.caballo_id.data = jya.caballo.id

        if jya.auxiliar_pista is not None:
            form.auxiliar_pista_id.data = jya.auxiliar_pista.id

        form.dias.data = [dia.id for dia in jya.dias_asignados]

    if request.method == "POST":
        if form.validate_on_submit():
            jya.propuesta_trabajo = form.propuesta_trabajo.data
            jya.condicion = form.condicion.data
            jya.sede = form.sede.data
            jya.profesor_id = form.profesor_id.data
            jya.conductor_caballo_id = form.conductor_caballo_id.data
            jya.caballo_id = form.caballo_id.data
            jya.auxiliar_pista_id = form.auxiliar_pista_id.data
            jya.dias_asignados = [
                obtener_dia(dia)
                for dia in form.dias.data
            ]
            guardar_cambios()
            flash("Jinete/Amazona: Información actualizada con éxito", "exito")
            return redirect(url_for("jinetes_y_amazonas.ver", id=id))
        else:
            flash("Error al actualizar jinete/amazona", "error")

    return render_template(
        "pages/jinetes_y_amazonas/nuevo_j_y_a_inst.html",
        form=form,
        jya=jya,
        titulo="Editar información institucional - J/A "
        + str(jya.nombre)
        + " "
        + str(jya.apellido),
    )


@bp.route("/nuevo_familiar/<int:jya_id>", methods=["GET", "POST"])
@chequear_permiso("jya_crear")
@sesion_iniciada_requerida
def nuevo_familiar(jya_id: int):
    """
    Controlador para la carga de un familiar de jinete/amazona
    """
    form = FamiliarForm(jya_id)
    jya = encontrar_jya(jya_id)

    if request.method == "POST":
        if form.validate_on_submit():
            jya_id = jya_id
            nombre = form.nombre.data
            apellido = form.apellido.data
            parentesco = form.parentesco.data
            dni = form.dni.data
            domicilio = form.domicilio_actual.data
            telefono = form.telefono_actual.data
            email = form.email.data
            nivel_escolaridad = form.nivel_escolaridad.data
            ocupacion = form.ocupacion.data
            crear_familiar(
                jya_id,
                nombre,
                apellido,
                parentesco,
                dni,
                domicilio,
                telefono,
                email,
                nivel_escolaridad,
                ocupacion
            )
            flash("Familiar cargado con éxito", "exito")
            return redirect(url_for("jinetes_y_amazonas.ver_familiares",
                                    id=jya_id))
        else:
            flash("Error al crear el familiar")

    return render_template("pages/jinetes_y_amazonas/crear_familiar.html",
                           form=form,
                           jya=jya,
                           titulo="Cargar familiar de " +
                           jya.nombre+" "+jya.apellido)


@bp.get("<int:id>/familiares")
@chequear_permiso("jya_listar")
@sesion_iniciada_requerida
def ver_familiares(id: int):
    """
    Controlador que devuelve el listado de
    familiares del jinete/amazona
    """
    jya = encontrar_jya(id)
    orden = request.args.get("orden", "asc")
    ordenar_por = request.args.get("ordenar_por", "id")
    pagina = convertir_a_entero(request.args.get("pagina", 1))
    cant_por_pagina = convertir_a_entero(
        request.args.get("cant_por_pagina", 6))
    familiares, cant_resultados = listar_familiares(
        jya.id,
        ordenar_por,
        orden,
        pagina,
        cant_por_pagina
    )

    cant_paginas = cant_resultados // cant_por_pagina
    if cant_resultados % cant_por_pagina != 0:
        cant_paginas += 1

    return render_template(
        "pages/jinetes_y_amazonas/ver_familiares.html",
        jya=jya,
        familiares=familiares,
        cant_resultados=cant_resultados,
        cant_paginas=cant_paginas,
        pagina=pagina,
        orden=orden,
        ordenar_por=ordenar_por
    )


@bp.route("/editar_familiar/<int:id>", methods=["GET", "POST"])
@chequear_permiso("jya_crear")
@sesion_iniciada_requerida
def editar_familiar(id: int):
    familiar = encontrar_familiar(id)
    form = FamiliarForm(obj=familiar)

    if request.method == "GET":
        form.nivel_escolaridad.data = familiar.nivel_escolaridad.name

    if request.method == "POST":
        if form.validate_on_submit():
            familiar.nombre = form.nombre.data
            familiar.apellido = form.apellido.data
            familiar.parentesco = form.parentesco.data
            familiar.dni = form.dni.data
            familiar.domicilio = form.domicilio_actual.data
            familiar.telefono = form.telefono_actual.data
            familiar.email = form.email.data
            familiar.nivel_escolaridad = form.nivel_escolaridad.data
            familiar.ocupacion = form.ocupacion.data
            guardar_cambios()

            flash("Datos actualizados con éxito", "exito")
            return redirect(url_for("jinetes_y_amazonas.ver_familiares",
                                    id=familiar.jya_id))
        else:
            flash("Ocurrió un error al actualizar los datos del familiar",
                  "error")
    return render_template("/pages/jinetes_y_amazonas/crear_familiar.html",
                           form=form,
                           jya=familiar.jya,
                           titulo="Editar familiar de " +
                           familiar.jya.nombre + " " + familiar.jya.apellido)


@bp.get("/familiar/<int:id>")
@chequear_permiso("jya_mostrar")
@sesion_iniciada_requerida
def ver_familiar(id: int):
    familiar = encontrar_familiar(id)
    jya = familiar.jya
    return render_template("/pages/jinetes_y_amazonas/ver_familiar.html",
                           familiar=familiar, jya=jya)
