import string
from flask import render_template, request, redirect, url_for, send_file, flash
from flask import Blueprint
from flask import current_app
from os import fstat
from src.core.jinetes_y_amazonas import (listar_j_y_a, crear_j_o_a, cargar_informacion_salud, cargar_informacion_economica, cargar_informacion_escuela, cargar_informacion_institucional, eliminar_jya, encontrar_jya, cargar_archivo,encontrar_archivos_de_jya, encontrar_archivo, listar_documentos, listar_tipos_de_documentos, listar_diagnosticos, listar_profesores, listar_conductores, listar_auxiliares_pista, listar_caballos, obtener_documento, eliminar_documento_j_y_a, guardar_cambios)
from src.core.jinetes_y_amazonas.jinetes_y_amazonas import JineteOAmazona, Diagnostico
from core.forms.forms_jinetes import NuevoJYAForm, InfoSaludJYAForm, InfoEconomicaJYAForm, InfoEscolaridadJYAForm,InfoInstitucionalJYAForm
from core.forms.forms_documentos_jya import SubirArchivoForm, EnlaceForm, EditarArchivoForm

import ulid
from io import BytesIO
from src.web.handlers.decoradores import sesion_iniciada_requerida, chequear_permiso

bp = Blueprint("jinetes_y_amazonas", __name__, url_prefix="/jinetes_y_amazonas")

'''
    Retorna los jinetes y amazonas
'''

@bp.get("/")
@chequear_permiso("jya_listar")
@sesion_iniciada_requerida
def listar():
    '''
        Controlador que muestra el listado de jinetes y amazonas del sistema.
    '''
    orden = request.args.get("orden", "asc")
    ordenar_por = request.args.get("ordenar_por", "id")
    pagina = int(request.args.get('pagina', 1))
    cant_por_pag = int(request.args.get('por_pag',6))
    nombre_filtro = request.args.get("nombre", "")
    apellido_filtro = request.args.get("apellido", "")
    dni_filtro = request.args.get("dni", "")
    profesionales_a_cargo = request.args.get("profesionales_a_cargo", "")

    jinetes = listar_j_y_a(nombre_filtro, apellido_filtro, dni_filtro, profesionales_a_cargo, ordenar_por, orden,pagina, cant_por_pag)
    cant_resultados = len(jinetes.items)
    cant_paginas = cant_resultados // cant_por_pag
    if cant_resultados % cant_por_pag != 0:
        cant_paginas += 1
    
    return render_template(
        "jinetes_y_amazonas/listar.html",
        jinetes=jinetes,
        cant_resultados=cant_resultados,
        cant_paginas=cant_paginas,
        pagina=pagina,
        orden=orden,
        ordenar_por=ordenar_por,
        nombre_filtro=nombre_filtro,
        apellido_filtro=apellido_filtro,
        dni_filtro=dni_filtro,
        profesionales_a_cargo=profesionales_a_cargo
    )

@bp.route("/nuevo_joa", methods=["GET", "POST"])
@chequear_permiso("jya_crear")
@sesion_iniciada_requerida
def nuevo_j_y_a():
    '''
        Controlador que muestra el formulario de alta de un jinete o amazona o guarda los datos ingresados en él.
    '''
    form = NuevoJYAForm()
    form.submit.label.text = "Continuar"

    if form.validate_on_submit():
        nombre = form.nombre.data
        apellido = form.apellido.data
        dni = form.dni.data
        edad = form.edad.data
        fecha_nacimiento = form.fecha_nacimiento.data
        provincia_nacimiento = form.provincia_nacimiento.data
        localidad_nacimiento = form.localidad_nacimiento.data
        domicilio_actual = form.domicilio_actual.data
        telefono_actual = form.telefono_actual.data
        contacto_emer_nombre = form.contacto_emer_nombre.data
        contacto_emer_telefono = form.contacto_emer_telefono.data
        jya_nuevo = crear_j_o_a(nombre, apellido, dni, edad, fecha_nacimiento, provincia_nacimiento, localidad_nacimiento, domicilio_actual, telefono_actual, contacto_emer_nombre, contacto_emer_telefono)

        flash("Nuevo J&A creado. Continúe con la carga de información", "exito")
        return redirect(url_for('jinetes_y_amazonas.cargar_info_salud', id=jya_nuevo.id))

    return render_template("jinetes_y_amazonas/nuevo_j_y_a.html", form=form, titulo="Nuevo jinete/amazona")

@bp.route("/cargar_info_salud/<int:id>", methods=["GET", "POST"])
@chequear_permiso("jya_crear")
@sesion_iniciada_requerida
def cargar_info_salud(id: int):
    '''
        Controlador que muestra muestra el formulario de alta de la información de salud del jinete o amazona o guarda los datos asociados a él.
    '''
    form = InfoSaludJYAForm()
    form.diagnostico.choices = [(diagnostico.id, diagnostico.nombre) for diagnostico in listar_diagnosticos()]
    form.submit.label.text = "Continuar"

    if form.validate_on_submit():
        certificado_discapacidad = form.certificado_discapacidad.data
        diagnostico_id = form.diagnostico.data
        diagnostico_otro = form.diagnostico_otro.data
        tipo_discapacidad = form.tipo_discapacidad.data
        cargar_informacion_salud(id, certificado_discapacidad, diagnostico_id, diagnostico_otro, tipo_discapacidad)
        flash("Información de salud guardada. Continúe con la carga.", "exito")

        return redirect(url_for('jinetes_y_amazonas.cargar_info_econ', id=id))

    return render_template("jinetes_y_amazonas/nuevo_j_y_a_salud.html", form=form, titulo="Nuevo jinete/amazona")

@bp.route("/cargar_info_econ/<int:id>", methods=["GET", "POST"])
@chequear_permiso("jya_crear")
@sesion_iniciada_requerida
def cargar_info_econ(id : int):
    '''
        Controlador que muestra el formulario de carga de la información económica del jinete o amazona, o guarda los datos ingrsados en él.
    '''
    form = InfoEconomicaJYAForm()
    form.submit.label.text = "Continuar"

    if form.validate_on_submit():
        asignacion_familiar = form.asignacion_familiar.data
        tipo_asignacion_familiar = form.tipo_asignacion_familiar.data
        beneficiario_pension = form.beneficiario_pension.data
        tipo_pension = form.tipo_pension.data
        obra_social = form.obra_social.data
        num_afiliado = form.num_afiliado.data
        posee_curatela = form.posee_curatela.data
        observaciones_obra_social = form.observaciones_obra_social.data

        cargar_informacion_economica(id, asignacion_familiar, tipo_asignacion_familiar, beneficiario_pension,tipo_pension, obra_social, num_afiliado, posee_curatela, observaciones_obra_social)
        flash("Información económica guardada. Continúe con la carga", "exito")
        return redirect(url_for('jinetes_y_amazonas.cargar_info_esc', id= id))
    return render_template("jinetes_y_amazonas/nuevo_j_y_a_econ.html", form=form, titulo="Nuevo jinete/amazona")

@bp.route("/cargar_info_esc/<int:id>", methods=["GET", "POST"])
@chequear_permiso("jya_crear")
@sesion_iniciada_requerida
def cargar_info_esc(id : int):
    '''
        Controlador que muestra el formulario para la carga de información de escolaridad del jinete o amazona, o guarda los datos cargados en él.
    '''
    form = InfoEscolaridadJYAForm()
    form.submit.label.text = "Continuar"

    if form.validate_on_submit():
        nombre_escuela = form.nombre_escuela.data
        direccion_escuela = form.direccion_escuela.data
        telefono_escuela = form.telefono_escuela.data
        grado_escuela = form.grado_escuela.data
        observaciones_escuela = form.observaciones_escuela.data
        profesionales_a_cargo = form.profesionales_a_cargo.data
        cargar_informacion_escuela(id, nombre_escuela, direccion_escuela, telefono_escuela, grado_escuela, observaciones_escuela, profesionales_a_cargo)
        flash("Informacion de escolaridad guardada. Continúe con la carga.", "exito")
        return redirect(url_for('jinetes_y_amazonas.cargar_info_inst', id = id))
    return render_template("jinetes_y_amazonas/nuevo_j_y_a_esc.html", form=form, titulo="Nuevo jinete/amazona")


@bp.route("/cargar_info_inst/<int:id>", methods=["GET", "POST"])
@chequear_permiso("jya_crear")
@sesion_iniciada_requerida
def cargar_info_inst(id : int):
    '''
        Controlador que muestra el formulario para la carga de información institucional del jinete o amazona, o guarda los datos cargados en él.
    '''
    form = InfoInstitucionalJYAForm()
    form.submit.label.text = "Finalizar"

    form.profesor_id.choices = [(profesor.id, profesor.nombre) for profesor in listar_profesores()]
    form.conductor_caballo_id.choices = [(conductor.id, conductor.nombre) for conductor in listar_conductores()]
    form.caballo_id.choices = [(caballo.id, caballo.nombre) for caballo in listar_caballos()]
    form.auxiliar_pista_id.choices = [(auxiliar.id, auxiliar.nombre) for auxiliar in listar_auxiliares_pista()]
    if form.validate_on_submit():
        propuesta_de_trabajo = form.propuesta_trabajo.data
        condicion = form.condicion.data
        sede = form.sede.data
        profesor_id = form.profesor_id.data
        conductor_caballo_id = form.profesor_id.data
        caballo_id = form.caballo_id.data
        auxiliar_pista_id = form.auxiliar_pista_id.data
        dias = form.dias.data
        cargar_informacion_institucional(id, propuesta_de_trabajo, condicion, sede, dias, profesor_id, conductor_caballo_id, caballo_id, auxiliar_pista_id)
        
        flash("Información institucional guardada. Continúe con la carga.", "exito")
        return redirect(url_for('jinetes_y_amazonas.listar'))
    
    return render_template("jinetes_y_amazonas/nuevo_j_y_a_inst.html", form=form, titulo="Nuevo jinete/amazona")
 

@bp.get("/<int:id>/")
@chequear_permiso("jya_mostrar")
@sesion_iniciada_requerida
def ver(id: int):
    '''
        Controlador que permite visualizar la información de un jinete o amazona.
    '''
    jya = encontrar_jya(id)

    return render_template("jinetes_y_amazonas/ver_jya.html", jya=jya)


@bp.get("/<int:id>/eliminar/")
@chequear_permiso("jya_eliminar")
@sesion_iniciada_requerida
def eliminar(id: int):
    '''
        Controlador que elimina un jinete o amazona y redirige al listado de jinetes y amazonas
    '''
    eliminar_jya(id)

    flash("J&A eliminado con éxito.", "exito")
    return redirect(url_for("jinetes_y_amazonas.listar"))

@bp.route("/<int:id>/subir_archivo/", methods=["GET", "POST"])
@chequear_permiso("jya_crear")
@sesion_iniciada_requerida
def subir_archivo(id: int):
    '''
        Controlador que muestra el formulario para el alta de un archivo en el sistema.
    '''

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
            cliente.put_object("grupo17", url, archivo, tamaño, content_type = archivo.content_type)
            print(url)
            cargar_archivo(jya_id, titulo,tipo_archivo,url, archivo_externo = False)
            flash("Archivo subido con éxito", "exito")

            return redirect(url_for("jinetes_y_amazonas.ver_archivos", id=id))
        else:
            flash("Error al subir el archivo", "error")
    return render_template(
        "jinetes_y_amazonas/documentos.html",
        form=form,
        jya= id,
        titulo="Subir archivo",
        subir_archivo=True,
    )

@bp.route("/<int:id>/subir_enlace/", methods=["GET", "POST"])
@chequear_permiso("jya_crear")
@sesion_iniciada_requerida
def subir_enlace(id: int):
    '''
        Controlador que muestra el formulario para el alta de un archivo externo en el sistema (enlace a un archivo externo).
    '''
    
    form = EnlaceForm()

    if request.method == "POST":
        if form.validate_on_submit():
            titulo = form.titulo.data
            jya_id = id
            url = form.url.data
            tipo_archivo = form.tipo_de_documento_id.data
            cargar_archivo(jya_id, titulo, tipo_archivo, url, archivo_externo=True)

            flash("Enlace a documento subido con exito", "exito")
            return redirect(url_for("jinetes_y_amazonas.ver_archivos", id=id))
        else:
            flash("Error al subir el documento", "error")

    return render_template(
        "jinetes_y_amazonas/documentos.html",
        form=form,
        jya= id,
        titulo="Subir enlace",
        subir_enlace=True,
    )

@bp.get("/<int:id>/archivos")
@chequear_permiso("jya_mostrar")
@sesion_iniciada_requerida
def ver_archivos(id: int):
    '''
        Controlador que devuelve el listado de archivos asociados a un jinete o amazona.
    '''
    archivos = encontrar_archivos_de_jya(id)
    jya = encontrar_jya(id)
    orden = request.args.get("orden", "asc")
    ordenar_por = request.args.get("ordenar_por", "id")
    pagina = int(request.args.get("pagina", 1))
    cant_por_pagina = int(request.args.get("cant_por_pagina", 10))
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
        "jinetes_y_amazonas/ver_documentos.html",
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


@bp.get("/<int:jya_id>/archivos/<int:archivo_id>/editar/")
@chequear_permiso("jya_actualizar")
@sesion_iniciada_requerida
def editar_archivo(jya_id: int, archivo_id:int):
    '''
        Controlador que muestra el formulario para la edición de un archivo o enlace.
    '''
    archivo = encontrar_archivo(archivo_id)
    flash("Funcionalidad no implementada")
    return render_template("jinetes_y_amazonas/documentos.html", jya = archivo.jya)

@bp.get("/descargar_archivo/<int:archivo_id>")
@chequear_permiso("jya_mostrar")
@sesion_iniciada_requerida
def descargar_archivo(archivo_id:int):
    '''
        Controlador que permite la descarga de un archivo dado su id.
    '''
    documento = obtener_documento(archivo_id)
    cliente = current_app.storage.client
    archivo = cliente.get_object("grupo17", documento.url)
    archivo_bytes = BytesIO(archivo.read())
    extension = f".{documento.url.split('.')[-1]}" if "." in documento.url else ""

    return send_file(archivo_bytes,
        as_attachment=True,
        download_name=f"{documento.titulo}{extension}")

@bp.get("/eliminar_documento/<int:id>")
@chequear_permiso("jya_eliminar")
@sesion_iniciada_requerida
def eliminar_documento(id:int):
    '''
        Controlador que permite la eliminación de un documento y redirige a la vista de listado de archivos.
    '''
    doc = eliminar_documento_j_y_a(id)
    flash("Documento eliminado con éxito")

    return redirect(url_for("jinetes_y_amazonas.ver_archivos", id=doc.jya_id))

@bp.route("/<int:id>/editar", methods=["GET", "POST"])
@chequear_permiso("jya_actualizar")
@sesion_iniciada_requerida
def editar_j_y_a(id: int):
    '''
        Controlador que muestra permite editar la información general del jinete o amazona.
    '''
    jya = encontrar_jya(id)
    form = NuevoJYAForm(obj=jya)
    form.submit.label.text= "Guardar"
    if request.method == "POST":
        if form.validate_on_submit():
            jya.nombre = form.nombre.data
            jya.apellido = form.apellido.data
            jya.dni = form.dni.data
            jya.edad = form.edad.data
            jya.fecha_nacimiento = form.fecha_nacimiento.data
            jya.provincia_nacimiento = form.provincia_nacimiento.data
            jya.localidad_nacimiento = form.localidad_nacimiento.data
            jya.domicilio_actual = form.domicilio_actual.data
            jya.telefono_actual = form.telefono_actual.data
            jya.contacto_emer_nombre = form.contacto_emer_nombre.data
            jya.contacto_emer_telefono = form.contacto_emer_telefono.data
            guardar_cambios()
            flash("Jinete/Amazona: Información actualizada con éxito", "exito")
            return redirect(url_for('jinetes_y_amazonas.ver', id=id))
        else:
            flash("Error al actualizar jinete/amazona","error")

    return render_template("jinetes_y_amazonas/nuevo_j_y_a.html", form=form, titulo= "Editar jinete/amazona" + str(jya.nombre) + " " + str(jya.apellido))


@bp.route("/editar_info_salud/<int:id>", methods=["GET", "POST"])
@chequear_permiso("jya_actualizar")
@sesion_iniciada_requerida
def editar_info_salud(id: int):
    '''
        Controlador que muestra permite editar la información de salud del jinete o amazona.
    '''
    jya = encontrar_jya(id)
    form = InfoSaludJYAForm(obj=jya)
    form.diagnostico.choices = [(diagnostico.id, diagnostico.nombre) for diagnostico in listar_diagnosticos()]
    
    if jya.diagnostico != None:
        form.diagnostico.data = jya.diagnostico.id
    form.submit.label.text= "Guardar"

    if request.method == "POST":
        if form.validate_on_submit():
            jya.certificado_discapacidad = form.certificado_discapacidad.data
            jya.diagnostico_id = form.diagnostico.data
            jya.diagnostico_otro = form.diagnostico_otro.data
            jya.tipo_discapacidad = form.tipo_discapacidad.data
            guardar_cambios()

            flash("Jinete/Amazona: Información actualizada con éxito", "exito")
            return redirect(url_for('jinetes_y_amazonas.ver', id=id))
        else:
            flash("Error al actualizar jinete/amazona","error")

    return render_template("jinetes_y_amazonas/nuevo_j_y_a_salud.html", form=form, titulo="Editar información de salud - Jinete/Amazona "+str(jya.nombre)+ " "+str(jya.apellido))


@bp.route("/editar_info_econ/<int:id>", methods=["GET", "POST"])
@chequear_permiso("jya_actualizar")
@sesion_iniciada_requerida
def editar_info_econ(id : int):
    '''
        Controlador que muestra permite editar la información economica del jinete o amazona.
    '''
    jya = encontrar_jya(id)
    form = InfoEconomicaJYAForm(obj=jya)
    form.submit.label.text= "Guardar"

    if request.method == "POST":
        if form.validate_on_submit():
            jya.asignacion_familiar = form.asignacion_familiar.data
            jya.tipo_asignacion_familiar = form.tipo_asignacion_familiar.data
            jya.beneficiario_pension = form.beneficiario_pension.data
            jya.tipo_pension = form.tipo_pension.data
            jya.obra_social = form.obra_social.data
            jya.num_afiliado = form.num_afiliado.data
            jya.posee_curatela = form.posee_curatela.data
            jya.observaciones_obra_social = form.observaciones_obra_social.data

            guardar_cambios()
            flash("Jinete/Amazona: Información actualizada con éxito", "exito")
            return redirect(url_for('jinetes_y_amazonas.ver', id=id))
        else:
            flash("Error al actualizar jinete/amazona","error")
    return render_template("jinetes_y_amazonas/nuevo_j_y_a_econ.html", form=form, titulo="Editar información de salud - Jinete/Amazona "+str(jya.nombre)+ " "+str(jya.apellido))

@bp.route("/editar_info_esc/<int:id>", methods=["GET", "POST"])
@chequear_permiso("jya_actualizar")
@sesion_iniciada_requerida
def editar_info_esc(id : int):
    '''
        Controlador que muestra permite editar la información sobre escolaridad del jinete o amazona.
    '''
    jya = encontrar_jya(id)
    form = InfoEscolaridadJYAForm(obj=jya)
    form.submit.label.text= "Guardar"
    #form.diagnostico.data = jya.diagnostico.id
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
            return redirect(url_for('jinetes_y_amazonas.ver', id=id))
        else:
            flash("Error al actualizar jinete/amazona","error")
    
    return render_template("jinetes_y_amazonas/nuevo_j_y_a_esc.html", form=form, titulo="Editar información de salud - Jinete/Amazona "+str(jya.nombre)+ " "+str(jya.apellido))


@bp.route("/editar_info_inst/<int:id>", methods=["GET", "POST"])
@chequear_permiso("jya_actualizar")
@sesion_iniciada_requerida
def editar_info_inst(id : int):
    '''
        Controlador que muestra permite editar la información institucional relacionada al jinete o amazona.
    '''
    jya = encontrar_jya(id)
    form = InfoInstitucionalJYAForm(obj=jya)
    
    form.profesor_id.choices = [(profesor.id, profesor.nombre) for profesor in listar_profesores()]
    if jya.profesor != None:
        form.profesor.data = jya.profesor.id
    
    form.conductor_caballo_id.choices = [(conductor.id, conductor.nombre) for conductor in listar_conductores()]
    
    if jya.conductor_caballo != None:
        form.conductor_caballo_id.data = jya.conductor_caballo.id
    
    form.caballo_id.choices = [(caballo.id, caballo.nombre) for caballo in listar_caballos()]
    
    if jya.caballo != None:
        form.caballo.data = jya.caballo.id
    
    form.auxiliar_pista_id.choices = [(auxiliar.id, auxiliar.nombre) for auxiliar in listar_auxiliares_pista()]
    
    if jya.auxiliar_pista != None:
        form.auxiliar_pista.data = jya.auxiliar_pista.id
    
    form.submit.label.text= "Guardar"

    if request.method == "POST":
        if form.validate_on_submit():
            jya.propuesta_de_trabajo = form.propuesta_trabajo.data
            jya.condicion = form.condicion.data
            jya.sede = form.sede.data
            jya.profesor_id = form.profesor_id.data
            jya.conductor_caballo_id = form.profesor_id.data
            jya.caballo_id = form.caballo_id.data
            jya.auxiliar_pista_id = form.auxiliar_pista_id.data
            #jya.dias = form.dias.data
            guardar_cambios()
            flash("Jinete/Amazona: Información actualizada con éxito", "exito")
            return redirect(url_for('jinetes_y_amazonas.ver', id=id))
        else:
            flash("Error al actualizar jinete/amazona","error")
    
    return render_template("jinetes_y_amazonas/nuevo_j_y_a_inst.html", form=form, titulo="Editar información de salud - Jinete/Amazona "+str(jya.nombre)+ " "+str(jya.apellido))
 