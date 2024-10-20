from datetime import datetime
from src.core.pago.pago_forms import PagoForm
from flask import Blueprint, render_template, request, redirect, url_for, flash
from src.core.pago import TipoDePago, Pago, crear_pago, listar_pagos, obtener_pago, guardar_cambios
from src.core.miembro import Miembro
from src.core.database import db


bp = Blueprint('pago', __name__, url_prefix='/pagos')


@bp.get("/")
def pago_listar():
    orden = request.args.get("orden", "asc")
    ordenar_por = request.args.get("ordenar_por", "fechaDePago")
    pagina = int(request.args.get("pagina", 1))
    cant_por_pagina = int(request.args.get("cant_por_pagina", 10))
    search_fecha_inicio = request.args.get("fecha_inicio", "")
    search_fecha_fin = request.args.get("fecha_fin", "")
    tipo_pago_id = request.args.get("tipo_pago_id", "")
    search_beneficiario = request.args.get("beneficiario", "")

    pagos, cant_resultados = listar_pagos(
        search_fecha_inicio, search_fecha_fin, tipo_pago_id, search_beneficiario, ordenar_por, orden, pagina, cant_por_pagina
    )

    tipos_pago = TipoDePago.query.all()

    if cant_resultados == 0:
        cant_paginas = 1
    else:
        cant_paginas = cant_resultados // cant_por_pagina
        if cant_resultados % cant_por_pagina != 0:
            cant_paginas += 1

    return render_template(
        "pagos/listar.html",
        pagos=pagos,
        tipos_pago=tipos_pago,
        cant_resultados=cant_resultados,
        cant_paginas=cant_paginas,
        pagina=pagina,
        orden=orden,
        ordenar_por=ordenar_por,
        fecha_inicio=search_fecha_inicio,
        fecha_fin=search_fecha_fin,
        tipo_pago_id=tipo_pago_id,
        beneficiario=search_beneficiario,
    )

@bp.route('/crear', methods=['GET', 'POST'])
def pago_crear():
    form = PagoForm()
    form.tipo_id.choices = [(tipo.id, tipo.nombre) for tipo in TipoDePago.query.all()]
    
    if form.validate_on_submit():
        monto = form.monto.data
        descripcion = form.descripcion.data
        fechaDePago = form.fechaDePago.data
        tipo_id = form.tipo_id.data

        tipo_pago = TipoDePago.query.get(tipo_id)
        miembro_dni = form.dni.data if tipo_pago.nombre == 'Honorario' else None

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

    return render_template('pagos/crear.html', form=form)


@bp.route('/<int:id>', methods=['GET'])
def pago_mostrar(id):
    pago = Pago.query.get_or_404(id)
    if pago.miembro_id:
        miembro = Miembro.query.filter_by(id=pago.miembro_id).first()
        beneficiario= miembro.dni
    else:
        beneficiario = ''
    return render_template('pagos/mostrar.html', pago=pago, beneficiario=beneficiario)

@bp.route('/<int:id>/eliminar', methods=['GET'])
def pago_eliminar(id):
    pago = Pago.query.get_or_404(id)
    db.session.delete(pago)
    db.session.commit()
    flash("Pago eliminado con exito.", 'success')
    return redirect(url_for('pago.pago_listar'))

@bp.route("/<int:id>/editar/", methods=["GET", "POST"])
def pago_editar(id: int):
    pago = obtener_pago(id)
    form = PagoForm(obj=pago)
    if (pago.miembro_id != None):
        form.dni.data = pago.miembro.dni
    form.tipo_id.choices = [(tipo.id, tipo.nombre) for tipo in TipoDePago.query.all()]

    if form.validate_on_submit():
        pago.tipo_id = form.tipo_id.data
        pago.monto = form.monto.data
        pago.descripcion = form.descripcion.data
        pago.fechaDePago = form.fechaDePago.data
        

        tipo_pago = TipoDePago.query.get(form.tipo_id.data)
        miembro_dni = form.dni.data if tipo_pago.nombre == 'Honorario' else None
        miembro_id = None
        if miembro_dni:
            miembro = Miembro.query.filter_by(dni=miembro_dni).first()
            if miembro:
                miembro_id = miembro.id
            else:
                flash(f"No se encontró ningún miembro con el DNI {miembro_dni}.", 'danger')
                return render_template("pagos/crear.html", form=form)
        pago.miembro_id = miembro_id    

        guardar_cambios()
        return redirect(url_for("pago.pago_listar"))

    return render_template("pagos/crear.html", form=form)
