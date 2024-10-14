from flask import Blueprint, render_template, request, redirect, url_for
from src.core.miembro import Miembro, Profesion, CondicionDeTrabajo, PuestoLaboral, listar_miembros, crear_miembro
from sqlalchemy import asc, desc
from src.core.database import db

miembro_bp = Blueprint('miembro', __name__, url_prefix='/miembros')

@miembro_bp.route('/', methods=['GET'])
def index_miembros():
    miembros = listar_miembros()
    return render_template('miembros/index.html', miembros=miembros)

@miembro_bp.route('/create', methods=['GET', 'POST'])
def create_miembro():
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
        activo = request.form.get('activo') == 'on'
        
        crear_miembro(nombre=nombre, apellido=apellido, dni=dni, email=email, telefono=telefono,
            nombreContactoEmergencia=nombreContactoEmergencia, telefonoContactoEmergencia=telefonoContactoEmergencia,
            obraSocial=obraSocial, numeroAfiliado=numeroAfiliado, profesion_id=profesion_id,
            condicion_id=condicion_id, puesto_laboral_id=puesto_laboral_id, activo=activo)

        return redirect(url_for('index_miembros'))

    return render_template('miembros/create.html', profesiones=profesiones, condiciones=condiciones, puestos=puestos)


@miembro_bp.route('//<int:id>', methods=['GET'])
def show_miembro(id):
    miembro = Miembro.query.get_or_404(id)
    return render_template('miembros/show.html', miembro=miembro)

@miembro_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit_miembro(id):
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
        return redirect(url_for('index_miembros'))

    return render_template('miembros/edit.html', miembro=miembro, profesiones=profesiones, condiciones=condiciones, puestos=puestos)

@miembro_bp.route('/<int:id>/eliminar', methods=['POST'])
def destroy_miembro(id):
    miembro = Miembro.query.get_or_404(id)
    db.session.delete(miembro)
    db.session.commit()
    return redirect(url_for('index_miembros'))
