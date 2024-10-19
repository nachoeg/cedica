from flask import Blueprint, render_template, request, redirect, url_for, flash
from src.core.miembro import Miembro, Profesion, CondicionDeTrabajo, PuestoLaboral, Domicilio
from src.core.miembro import listar_condiciones, listar_profesiones, listar_puestos_laborales, listar_miembros
from src.core.usuarios import Usuario
from sqlalchemy import asc, desc
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
    profesiones = Profesion.query.all()
    condiciones = CondicionDeTrabajo.query.all()
    puestos = PuestoLaboral.query.all()
    
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        dni = request.form['dni']
        email = request.form['email']
        telefono = request.form['telefono']
        nombreContactoEmergencia = request.form['nombreContactoEmergencia']
        telefonoContactoEmergencia = request.form['telefonoContactoEmergencia']
        obraSocial = request.form['obraSocial']
        numeroAfiliado = request.form['numeroAfiliado']
        profesion_id = request.form['profesion_id']
        condicion_id = request.form['condicion_id']
        puesto_laboral_id = request.form['puesto_laboral_id']
        alias_usuario = request.form['usuario']
        activo = True

        # Captura los datos del formulario del domicilio
        calle = request.form['calle']
        numero = request.form['numero']
        piso = request.form.get('piso')  # opcional
        dpto = request.form.get('dpto')  # opcional
        localidad = request.form['localidad']

        # Buscar si existe un domicilio con los mismos datos
        domicilio_existente = Domicilio.query.filter_by(
            calle=calle,
            numero=numero,
            piso=piso,
            dpto=dpto,
            localidad=localidad
        ).first()
        
        if domicilio_existente:
            domicilio_id = domicilio_existente.id
        else:
            nuevo_domicilio = crear_domicilio(calle=calle, numero=numero, piso=piso, dpto=dpto, localidad=localidad)
            domicilio_id = nuevo_domicilio.id

        nuevo_miembro_data = {
            "nombre": nombre,
            "apellido": apellido,
            "dni": dni,
            "email": email,
            "telefono": telefono,
            "nombreContactoEmergencia": nombreContactoEmergencia,
            "telefonoContactoEmergencia": telefonoContactoEmergencia,
            "obraSocial": obraSocial,
            "numeroAfiliado": numeroAfiliado,
            "profesion_id": profesion_id,
            "condicion_id": condicion_id,
            "puesto_laboral_id": puesto_laboral_id,
            "domicilio_id": domicilio_id,
            "activo": True
        }

        if alias_usuario:
            usuario = Usuario.query.filter_by(alias=alias_usuario).first()
            if usuario:
                usuario_id = usuario.id
                nuevo_miembro_data["usuario_id"] = usuario_id


        # Crear el miembro con los datos recopilados
        crear_miembro(**nuevo_miembro_data)

        flash("Miembro creado con exito.", 'success')
        return redirect(url_for('miembro.miembro_listar'))

    return render_template('miembros/crear.html', profesiones=profesiones, condiciones=condiciones, puestos=puestos)


@bp.route('/<int:id>/mostrar', methods=['GET'])
def miembro_mostrar(id):
    miembro = Miembro.query.get_or_404(id)
    return render_template('miembros/mostrar.html', miembro=miembro)

@bp.route('/<int:id>/editar', methods=['GET', 'POST'])
def miembro_editar(id):
    miembro = Miembro.query.get_or_404(id)
    profesiones = Profesion.query.all()
    condiciones = CondicionDeTrabajo.query.all()
    puestos = PuestoLaboral.query.all()

    if request.method == 'POST':
        miembro.nombre = request.form['nombre'] or miembro.nombre
        miembro.apellido = request.form['apellido'] or miembro.apellido
        miembro.dni = request.form['dni'] or miembro.dni
        miembro.email = request.form['email'] or miembro.email
        miembro.telefono = request.form['telefono'] or miembro.telefono
        miembro.nombreContactoEmergencia = request.form['nombreContactoEmergencia'] or miembro.nombreContactoEmergencia
        miembro.telefonoContactoEmergencia = request.form['telefonoContactoEmergencia'] or miembro.telefonoContactoEmergencia
        miembro.obraSocial = request.form['obraSocial'] or miembro.obraSocial
        miembro.numeroAfiliado = request.form['numeroAfiliado'] or miembro.numeroAfiliado
        miembro.profesion_id = request.form['profesion_id'] or miembro.profesion_id
        miembro.condicion_id = request.form['condicion_id'] or miembro.condicion_id
        miembro.puesto_laboral_id = request.form['puesto_laboral_id'] or miembro.puesto_laboral_id
        miembro.activo = request.form.get('activo') == 'on'
        
        db.session.commit()
        return redirect(url_for('miembro.miembro_listar'))

    return render_template('miembros/editar.html', miembro=miembro, profesiones=profesiones, condiciones=condiciones, puestos=puestos)

@bp.route('/<int:id>/eliminar', methods=['POST'])
def miembro_eliminar(id):
    miembro = Miembro.query.get_or_404(id)
    db.session.delete(miembro)
    db.session.commit()
    flash("Miembro eliminado con exito.", 'success')
    return redirect(url_for('miembro.miembro_listar'))
