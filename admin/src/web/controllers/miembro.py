from flask import Blueprint, render_template, request, redirect, url_for, flash
from src.core.miembro import Miembro, Profesion, CondicionDeTrabajo, PuestoLaboral, crear_domicilio, crear_miembro, Domicilio
from src.core.usuarios import Usuario
from sqlalchemy import asc, desc
from src.core.database import db

miembro_bp = Blueprint('miembro', __name__, url_prefix='/miembros')

@miembro_bp.route('/', methods=['GET'])
def miembro_listar():
    search_nombre = request.args.get('nombre', '')
    search_apellido = request.args.get('apellido', '')
    search_dni = request.args.get('dni', '')
    search_email = request.args.get('email', '')
    search_profesion = request.args.get('profesion', '')
    orden_campo = request.args.get('orden', 'nombre') 
    ascendente = request.args.get('asc', '1') == '1'
    pagina = int(request.args.get('page', 1))

    query = Miembro.query.join(Profesion).filter(
        Miembro.nombre.ilike(f"%{search_nombre}%"),
        Miembro.apellido.ilike(f"%{search_apellido}%"),
        Miembro.dni.ilike(f"%{search_dni}%"),
        Miembro.email.ilike(f"%{search_email}%"),
        Profesion.nombre.ilike(f"%{search_profesion}%")
    )

    if orden_campo in ['nombre', 'apellido', 'created_on']:  
        if ascendente:
            query = query.order_by(getattr(Miembro, orden_campo).asc())
        else:
            query = query.order_by(getattr(Miembro, orden_campo).desc())
    else:
        query = query.order_by(Miembro.nombre.asc())  

    miembros_paginados = query.paginate(page=pagina, per_page=10, error_out=False)

    return render_template(
        'miembros/listar.html',
        miembros_paginados=miembros_paginados, 
        ascendente=ascendente, 
        nombre=search_nombre,
        apellido=search_apellido,
        dni=search_dni,
        email=search_email,
        profesion=search_profesion,
        orden_campo=orden_campo
    )


@miembro_bp.route('/crear', methods=['GET', 'POST'])
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


@miembro_bp.route('/<int:id>/mostrar', methods=['GET'])
def miembro_mostrar(id):
    miembro = Miembro.query.get_or_404(id)
    return render_template('miembros/mostrar.html', miembro=miembro)

@miembro_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
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

@miembro_bp.route('/<int:id>/eliminar', methods=['POST'])
def miembro_eliminar(id):
    miembro = Miembro.query.get_or_404(id)
    db.session.delete(miembro)
    db.session.commit()
    flash("Miembro eliminado con exito.", 'success')
    return redirect(url_for('miembro.miembro_listar'))
