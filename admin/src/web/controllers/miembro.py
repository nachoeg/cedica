from flask import Blueprint, render_template, request, redirect, url_for, flash
from src.core.miembro import Miembro, Profesion, CondicionDeTrabajo, PuestoLaboral, Domicilio
from src.core.miembro import crear_miembro, crear_domicilio, listar_condiciones, listar_profesiones, listar_puestos_laborales, listar_miembros
from src.core.miembro.forms_miembro import InfoMiembroForm
from src.core.usuarios import Usuario
from src.core.database import db

bp = Blueprint('miembro', __name__, url_prefix='/miembros')

@bp.route('/', methods=['GET'])
def miembro_listar():
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
def miembro_crear():
    form = InfoMiembroForm()
    
    form.condicion_id.choices = [(condicion.id, condicion.nombre) for condicion in CondicionDeTrabajo.query.all()]
    form.profesion_id.choices = [(profesion.id, profesion.nombre) for profesion in Profesion.query.all()]
    form.puesto_laboral_id.choices = [(puesto.id, puesto.nombre) for puesto in PuestoLaboral.query.all()]

    if form.validate_on_submit():
        nombre = form.nombre.data
        apellido = form.apellido.data
        dni = form.dni.data
        email = form.email.data
        telefono = form.telefono.data
        nombre_contacto_emergencia = form.nombreContactoEmergencia.data
        telefono_contacto_emergencia = form.telefonoContactoEmergencia.data
        obra_social = form.obraSocial.data
        numero_afiliado = form.numeroAfiliado.data
        condicion_id = form.condicion_id.data
        profesion_id = form.profesion_id.data
        puesto_laboral_id = form.puesto_laboral_id.data
        calle = form.calle.data
        numero = form.numero.data
        piso = form.piso.data
        dpto = form.dpto.data
        localidad = form.localidad.data
        alias = form.alias.data

        domicilio_existente = Domicilio.query.filter_by(
            calle=calle,
            numero=numero,
            piso=piso,
            dpto=dpto,
            localidad=localidad
        ).first

        if domicilio_existente:
            domicilio_id = domicilio_existente.id
        else:
            nuevo_domicilio = crear_domicilio(calle=calle, numero=numero, piso=piso, dpto=dpto, localidad=localidad)
            domicilio_id = nuevo_domicilio.id

        if alias:
            usuario = Usuario.query.filter_by(alias=alias_usuario).first()
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

    return render_template('miembros/crear.html', form=form)

@bp.route('/<int:id>/mostrar', methods=['GET'])
def miembro_mostrar(id):
    miembro = Miembro.query.get_or_404(id)
    return render_template('miembros/mostrar.html', miembro=miembro)

@bp.route('/<int:id>/eliminar', methods=['POST'])
def miembro_eliminar(id):
    miembro = Miembro.query.get_or_404(id)
    db.session.delete(miembro)
    db.session.commit()
    flash("Miembro eliminado con exito.", 'success')
    return redirect(url_for('miembro.miembro_listar'))
