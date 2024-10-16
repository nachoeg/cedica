from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from src.core.pago import TipoDePago, Pago, crear_pago
from src.core.miembro import Miembro


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