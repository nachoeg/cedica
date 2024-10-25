from io import BytesIO
from flask import (
    current_app, 
    Blueprint, 
    render_template, 
    request, 
    redirect, 
    url_for, 
    flash,
    send_file,
    abort)
from src.core.miembro import (
    crear_miembro, 
    crear_domicilio, 
    listar_condiciones, 
    listar_profesiones, 
    obtener_documento, 
    listar_puestos_laborales, 
    listar_miembros, 
    obtener_miembro, 
    guardar_cambios, 
    buscar_domicilio, 
    cambiar_condicion_miembro, 
    listar_tipos_de_documentos, 
    listar_documentos, 
    crear_documento,
    eliminar_documento_miembro,
    miembro_por_id)
from src.core.forms.miembro_forms import InfoMiembroForm, ArchivoMiembroForm, EnlaceMiembroForm, EditarArchivoMiembroForm
from src.core.usuarios import usuario_por_alias
from os import fstat
from src.web.handlers.decoradores import sesion_iniciada_requerida, chequear_permiso
import ulid

bp = Blueprint('miembro', __name__, url_prefix='/miembros')


@bp.route('/', methods=['GET'])
@chequear_permiso("miembro_listar")
@sesion_iniciada_requerida
def miembro_listar():
    """ Realiza el listado paginado de los miembros del equipo,
    permite filtrar por nombre, apellido, dni, email y profesion, ademas de ordenar
    asc y desc por nombre, apellido y fecha de creacion"""
    orden = request.args.get("orden", "asc")
    ordenar_por = request.args.get("ordenar_por", "nombre")
    pagina = int(request.args.get("pagina", 1))
    cant_por_pagina = int(request.args.get("cant_por_pagina", 10))
    nombre_filtro = request.args.get("nombre", "")
    apellido_filtro = request.args.get("apellido", "")
    dni_filtro = request.args.get("dni", "")
    email_filtro = request.args.get("email", "")
    profesion_filtro = request.args.get("profesion", "")

    miembros, cant_resultados = listar_miembros(
        nombre_filtro, apellido_filtro, dni_filtro, email_filtro, profesion_filtro,
        ordenar_por, orden, pagina, cant_por_pagina
    )

    profesiones = listar_profesiones()
    puestos = listar_puestos_laborales()
    condiciones = listar_condiciones()

    if cant_resultados == 0:
        cant_paginas = 1
    else:
        cant_paginas = cant_resultados // cant_por_pagina
        if cant_resultados % cant_por_pagina != 0:
            cant_paginas += 1

    return render_template(
        "miembros/listar.html",
        miembros=miembros,
        profesiones=profesiones,
        puestos=puestos,
        condiciones=condiciones,
        cant_resultados=cant_resultados,
        cant_paginas=cant_paginas,
        pagina=pagina,
        orden=orden,
        ordenar_por=ordenar_por,
        nombre_filtro=nombre_filtro,
        apellido_filtro=apellido_filtro,
        dni_filtro=dni_filtro,
        email_filtro=email_filtro,
        profesion_filtro=profesion_filtro
    )

@bp.route('/crear', methods=['GET', 'POST'])
@chequear_permiso("miembro_crear")
@sesion_iniciada_requerida
def miembro_crear():
    """ Levante el formulario para crear un miembro y recibe los datos que envia al modulo de miembro para crear uno nuevo"""
    form = InfoMiembroForm()

    form.condicion_id.choices = [(condicion.id, condicion.nombre) for condicion in listar_condiciones()]
    form.profesion_id.choices = [(profesion.id, profesion.nombre) for profesion in listar_profesiones()]
    form.puesto_laboral_id.choices = [(puesto.id, puesto.nombre) for puesto in listar_puestos_laborales()]

    if request.method == "POST" and form.validate_on_submit():
        nombre = form.nombre.data
        apellido = form.apellido.data
        dni = form.dni.data
        email = form.email.data
        telefono = form.telefono.data
        nombre_contacto_emergencia = form.nombre_contacto_emergencia.data
        telefono_contacto_emergencia = form.telefono_contacto_emergencia.data
        obra_social = form.obra_social.data
        numero_afiliado = form.numero_afiliado.data
        condicion_id = form.condicion_id.data
        profesion_id = form.profesion_id.data
        puesto_laboral_id = form.puesto_laboral_id.data
        calle = form.calle.data
        numero = form.numero.data
        piso = form.piso.data
        dpto = form.dpto.data
        localidad = form.localidad.data
        alias = form.alias.data

        domicilio_existente = buscar_domicilio(
            calle=calle,
            numero=numero,
            piso=piso,
            dpto=dpto,
            localidad=localidad
        )

        if domicilio_existente:
            domicilio_id = domicilio_existente.id
        else:
            nuevo_domicilio = crear_domicilio(calle=calle, numero=numero, piso=piso, dpto=dpto, localidad=localidad)
            domicilio_id = nuevo_domicilio.id

        if alias:
            usuario = usuario_por_alias(alias_usuario)
            if usuario:
                usuario_id = usuario.id
                alias_usuario = usuario_id
            else:
                flash(f"No se encontró ningún usuario con el alias {alias}.", 'danger')
                return redirect(url_for('miembro.miembro_crear'))
        else:
            usuario_id = None

        crear_miembro(
            nombre=nombre,
            apellido=apellido,
            dni=dni,
            email=email,
            telefono=telefono,
            nombre_contacto_emergencia=nombre_contacto_emergencia,
            telefono_contacto_emergencia=telefono_contacto_emergencia,
            obra_social=obra_social,
            numero_afiliado=numero_afiliado,
            condicion_id=condicion_id,
            profesion_id=profesion_id,
            puesto_laboral_id=puesto_laboral_id,
            domicilio_id=domicilio_id,
            usuario_id=usuario_id
        )

        flash("Miembro registrado con éxito.", 'success')
        return redirect(url_for('miembro.miembro_listar'))

    return render_template('miembros/crear.html', form=form, titulo="Crear miembro")

@bp.route("/<int:id>/editar/", methods=["GET", "POST"])
@chequear_permiso("miembro_actualizar")
@sesion_iniciada_requerida
def miembro_editar(id: int):
    """Levanta un formulario para editar un miembro con los datos precargados del mismo"""
    miembro = obtener_miembro(id)
    if miembro is None:
        abort(404)
    form = InfoMiembroForm(obj=miembro)
    form.calle.data = miembro.domicilio.calle
    form.numero.data = miembro.domicilio.numero
    form.piso.data = miembro.domicilio.piso
    form.dpto.data = miembro.domicilio.dpto
    form.localidad.data = miembro.domicilio.localidad
    if miembro.usuario != None:
        form.alias.data = miembro.usuario.alias 
    
    form.condicion_id.choices = [(condicion.id, condicion.nombre) for condicion in listar_condiciones()]
    form.profesion_id.choices = [(profesion.id, profesion.nombre) for profesion in listar_profesiones()]
    form.puesto_laboral_id.choices = [(puesto.id, puesto.nombre) for puesto in listar_puestos_laborales()]
    
    if request.method == "POST" and form.validate_on_submit():
        miembro.nombre = form.nombre.data
        miembro.apellido = form.apellido.data
        miembro.dni = form.dni.data
        miembro.email = form.email.data
        miembro.telefono = form.telefono.data
        miembro.nombre_contacto_emergencia = form.nombre_contacto_emergencia.data
        miembro.telefono_contacto_emergencia = form.telefono_contacto_emergencia.data
        miembro.obra_social = form.obra_social.data
        miembro.numero_afiliado = form.numero_afiliado.data
        miembro.condicion_id = form.condicion_id.data
        miembro.profesion_id = form.profesion_id.data
        miembro.puesto_laboral_id = form.puesto_laboral_id.data

        domicilio_existente = buscar_domicilio(
            calle=form.calle.data,
            numero=form.numero.data,
            piso=form.piso.data,
            dpto=form.dpto.data,
            localidad=form.localidad.data
        )

        if domicilio_existente:
            miembro.domicilio_id = domicilio_existente.id
        else:
            nuevo_domicilio = crear_domicilio(calle=form.calle.data, numero=form.numero.data, piso=form.piso.data, dpto=form.dpto.data, localidad=form.localidad.data)
            miembro.domicilio_id = nuevo_domicilio.id

        alias_usuario = form.alias.data
        if alias_usuario:
            usuario = usuario_por_alias(alias_usuario)
            if usuario:
                usuario_id = usuario.id
                alias_usuario = usuario_id
            else:
                flash(f"No se encontró ningún usuario con el alias {alias_usuario}.", 'danger')
                return render_template("miembros/crear.html", form=form)
        else:
            miembro.usuario_id = None      

        guardar_cambios()
        return redirect(url_for("miembro.miembro_listar")) 

    return render_template("miembros/crear.html", form=form, titulo="Editar miembro")    

@bp.route('/<int:id>', methods=['GET'])
@chequear_permiso("miembro_mostrar")
@sesion_iniciada_requerida
def miembro_mostrar(id):
    """Muestra la informacion de un miembro del equipo"""
    miembro = miembro_por_id(id)
    return render_template('miembros/mostrar.html', miembro=miembro)

@bp.route('/<int:id>/cambiar_condicion', methods=['GET'])
@chequear_permiso("miembro_eliminar")
@sesion_iniciada_requerida
def miembro_cambiar_condicion(id):
    """Activa o desactiva a un miembro del equipo"""
    cambiar_condicion_miembro(id)
    flash("Miembro activado/desactivado con exito.", 'success')
    return redirect(url_for('miembro.miembro_listar'))

@bp.get("/<int:id>/documentos/")
@chequear_permiso("miembro_mostrar")
@sesion_iniciada_requerida
def miembro_documentos(id: int):
    """Lista los documentos de un miembro del sistema y los muestra de forma paginada"""
    miembro = miembro_por_id(id)
    orden = request.args.get("orden", "asc")
    ordenar_por = request.args.get("ordenar_por", "id")
    pagina = int(request.args.get("pagina", 1))
    cant_por_pagina = int(request.args.get("cant_por_pagina", 10))
    nombre_filtro = request.args.get("nombre", "")
    tipo_filtro = request.args.get("tipo", "")

    documentos, cant_resultados = listar_documentos(
        miembro.id,
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
        "miembros/documentos.html",
        miembro=miembro,
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
@chequear_permiso("miembro_crear")
@sesion_iniciada_requerida
def miembro_subir_archivo(id: int):
    """Permite subir un archivo desde la computadora del usuario y guardarlo como un documento del miembro"""
    miembro = obtener_miembro(id)
    if miembro is None:
        abort(404)
    form = ArchivoMiembroForm()
    form.tipo_de_documento_id.choices = [(t.id, t.tipo) for t in listar_tipos_de_documentos()]

    if request.method == "POST":
        if form.validate_on_submit():
            nombre = form.nombre.data
            tipo = form.tipo_de_documento_id.data
            miembro_id = id
            archivo = request.files["archivo"]
            client = current_app.storage.client
            size = fstat(archivo.fileno()).st_size
            url = f"miembro/{ulid.new()}-{archivo.filename}"

            client.put_object(
                "grupo17",
                url,
                archivo,
                size,
                content_type=archivo.content_type,
            )

            crear_documento(nombre, tipo, url, miembro_id, archivo_externo=False)

            flash("Documento subido con exito", "exito")
            return redirect(url_for("miembro.miembro_documentos", id=id))
        else:
            flash("Error al subir el documento", "error")

    return render_template(
        "pages/ecuestre/formulario_documento.html", form=form, miembro=miembro, subir_archivo=True
    )

@bp.route("/<int:id>/documentos/subir_enlace/", methods=["GET", "POST"])
@chequear_permiso("miembro_crear")
@sesion_iniciada_requerida
def miembro_subir_enlace(id: int):
    """Guada un enlace como documento del miembro"""
    miembro = obtener_miembro(id)
    if miembro is None:
        abort(404)
    form = EnlaceMiembroForm()
    form.tipo_de_documento_id.choices = [(t.id, t.tipo) for t in listar_tipos_de_documentos()]

    if request.method == "POST":
        if form.validate_on_submit():
            nombre = form.nombre.data
            tipo = form.tipo_de_documento_id.data
            miembro_id = id
            url = form.url.data

            crear_documento(nombre, tipo, url, miembro_id, archivo_externo=True)

            flash("Documento subido con exito", "exito")
            return redirect(url_for("miembro.miembro_documentos", id=id))
        else:
            flash("Error al subir el documento", "error")

    return render_template(
        "pages/ecuestre/formulario_documento.html", form=form, miembro=miembro, subir_enlace=True
    )

@bp.get("/<int:id>/documentos/<int:documento_id>/ir/")
@chequear_permiso("miembro_mostrar")
@sesion_iniciada_requerida
def ir_documento(id: int,documento_id: int):
    """Redirigue al enlace previamente cargado como documento del miembro"""
    documento = obtener_documento(documento_id)
    return redirect(documento.url)

@bp.get("/<int:id>/documentos/<int:documento_id>/descargar/")
@chequear_permiso("miembro_mostrar")
@sesion_iniciada_requerida
def descargar_documento(id: int, documento_id: int):
    """Descarga el archivo previamente cargado como documento del miembro"""
    documento = obtener_documento(documento_id)
    client = current_app.storage.client
    archivo = client.get_object("grupo17", documento.url)

    archivo_bytes = BytesIO(archivo.read())

    extension = f".{documento.url.split('.')[-1]}" if "." in documento.url else ""

    return send_file(
        archivo_bytes,
        as_attachment=True,
        download_name=f"{documento.nombre}{extension}"
    )

@bp.get("/<int:id>/documentos/<int:documento_id>/eliminar/")
@chequear_permiso("miembro_eliminar")
@sesion_iniciada_requerida
def eliminar_documento(id: int, documento_id: int):
    """Elimina un documento asignado al miembro"""
    documento = obtener_documento(documento_id)
    client = current_app.storage.client
    client.remove_object("grupo17", documento_id.url)
    miembro = obtener_miembro(id)
    if miembro is None:
        abort(404)
    eliminar_documento_miembro(documento_id)
    flash("Documento eliminado con exito", "exito")
    return redirect(url_for("miembro.miembro_documentos", id=id))

@bp.route("/<int:id>/documentos/<int:documento_id>/editar/", methods=["GET", "POST"])
@chequear_permiso("miembro_actualizar")
@sesion_iniciada_requerida
def editar_documento(id: int, documento_id: int):
    """Permite modificar un documento, para los enlaces se permite modificar todos los valores, 
    mientras que para archivos se puede modificar solamente tipo y nombre"""
    miembro = obtener_miembro(id)
    if miembro is None:
        abort(404)
    documento = obtener_documento(documento_id)
    if documento.archivo_externo:
        form = EnlaceMiembroForm(obj=documento)
    else:
        form =  EditarArchivoMiembroForm(obj=documento)
    form.tipo_de_documento_id.choices = [
        (t.id, t.tipo) for t in listar_tipos_de_documentos()
    ]

    if request.method == "POST":
        if form.validate_on_submit():
            documento.nombre = form.nombre.data
            documento.tipo_de_documento_id = form.tipo_de_documento_id.data
            if documento.archivo_externo:
                documento.url = form.url.data
            guardar_cambios()
            flash("Documento actualizado con exito", "exito")
            return redirect(url_for("miembro.miembro_documentos", id=id))
        else:
            flash("Error al actualizar el documento", "error")

    return render_template(
        "pages/ecuestre/formulario_documento.html",
        form=form,
        miembro=documento.miembro,
        titulo=f"Editar documento #{documento_id}",
        subir_enlace=documento.archivo_externo,
    )