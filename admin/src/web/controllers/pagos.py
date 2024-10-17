from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from src.core.pago import TipoDePago, Pago, crear_pago
from src.core.miembro import Miembro
from src.core.database import db


pago_bp = Blueprint('pago', __name__, url_prefix='/pagos')

@pago_bp.route('/crear', methods=['GET', 'POST'])
def pago_crear():
    tipos_pagos = TipoDePago.query.all()
    fecha_hoy = datetime.today().strftime('%Y-%m-%d')
    
    if request.method == 'POST':
        monto = request.form['monto']
        descripcion = request.form['descripcion']
        fechaDePago = request.form['fechaDePago']
        tipo_id = request.form['tipo_id']

        tipo_pago = TipoDePago.query.get(tipo_id)
        miembro_dni = request.form.get('dni') if tipo_pago.nombre == 'Honorario' else None

        miembro_id = None
        if miembro_dni:
            miembro = Miembro.query.filter_by(dni=miembro_dni).first()
            if miembro:
                miembro_id = miembro.id
            else:
                flash(f"No se encontró ningún miembro con el DNI {miembro_dni}.", 'danger')
                return redirect(url_for('pago.pago_crear'))

        crear_pago(monto=monto, descripcion=descripcion, fechaDePago=fechaDePago, tipo_id=tipo_id, miembro_id=miembro_id)

        flash("Pago registrado con éxito.", 'success')
        return redirect(url_for('pago.pago_crear'))

    return render_template('pagos/crear.html', tipos_pagos=tipos_pagos, fecha_hoy=fecha_hoy)

@pago_bp.route('/')
def pago_listar():
    # Obtener parámetros de búsqueda y orden
    search_fecha_inicio = request.args.get('fecha_inicio', '')
    search_fecha_fin = request.args.get('fecha_fin', '')
    tipo_pago_id = request.args.get('tipo_pago_id', '')
    orden_campo = request.args.get('orden', 'fechaDePago')
    ascendente = request.args.get('asc', '1') == '1'
    pagina = int(request.args.get('pagina', 1))

    # Construir la consulta base
    query = Pago.query.join(TipoDePago)

    # Aplicar filtros de búsqueda
    if search_fecha_inicio:
        query = query.filter(Pago.fechaDePago >= datetime.strptime(search_fecha_inicio, '%Y-%m-%d'))
    if search_fecha_fin:
        query = query.filter(Pago.fechaDePago <= datetime.strptime(search_fecha_fin, '%Y-%m-%d'))
    if tipo_pago_id:
        query = query.filter(Pago.tipo_id == tipo_pago_id)

    # Ordenar los pagos
    query = query.order_by(getattr(Pago, orden_campo).asc() if ascendente else getattr(Pago, orden_campo).desc())

    # Paginación
    pagos_paginados = query.paginate(page=pagina, per_page=10)

    # Obtener todos los tipos de pago para el filtro
    tipos_pago = TipoDePago.query.all()

    return render_template('pagos/listar.html',
        pagos_paginados=pagos_paginados,
        orden_campo=orden_campo,
        ascendente=ascendente,
        pagina=pagina,
        tipos_pago=tipos_pago,
        fecha_inicio=search_fecha_inicio,
        fecha_fin=search_fecha_fin,
        tipo_pago_id=tipo_pago_id)

@pago_bp.route('/<int:id>/mostrar', methods=['GET'])
def pago_mostrar(id):
    pago = Pago.query.get_or_404(id)
    if pago.miembro_id:
        miembro = Miembro.query.filter_by(id=pago.miembro_id).first()
        beneficiario= miembro.dni
    else:
        beneficiario = ''
    return render_template('pagos/mostrar.html', pago=pago, beneficiario=beneficiario)

@pago_bp.route('/<int:id>/eliminar', methods=['POST'])
def pago_eliminar(id):
    pago = Pago.query.get_or_404(id)
    db.session.delete(pago)
    db.session.commit()
    flash("Pago eliminado con exito.", 'success')
    return redirect(url_for('pago.pago_listar'))