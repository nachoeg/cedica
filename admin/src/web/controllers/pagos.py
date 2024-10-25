from src.core.pago.pago_forms import PagoForm
from flask import Blueprint, render_template, request, redirect, url_for, flash
from src.core.pago import (
    crear_pago, 
    listar_pagos, 
    obtener_pago, 
    guardar_cambios, 
    listar_tipos_pagos, 
    obtener_tipo_pago, 
    eliminar_pago)
from src.core.miembro import obtener_miembro_dni, obtener_miembro
from src.web.handlers.decoradores import sesion_iniciada_requerida, chequear_permiso

bp = Blueprint('pago', __name__, url_prefix='/pagos')

@bp.get("/")
@chequear_permiso("pago_listar")
@sesion_iniciada_requerida
def pago_listar():
    """Lista los pagos de forma paginada, una cantidad de 10 por pagina, permite aplicar filtros y ordenar de manera
    ascendente y descendente por diversos campos"""
    orden = request.args.get("orden", "asc")
    ordenar_por = request.args.get("ordenar_por", "fecha_pago")
    pagina = int(request.args.get("pagina", 1))
    cant_por_pagina = int(request.args.get("cant_por_pagina", 10))
    search_fecha_inicio = request.args.get("fecha_inicio", "")
    search_fecha_fin = request.args.get("fecha_fin", "")
    tipo_pago_id = request.args.get("tipo_pago_id", "")
    search_beneficiario = request.args.get("beneficiario", "")

    pagos, cant_resultados = listar_pagos(
        search_fecha_inicio, search_fecha_fin, tipo_pago_id, search_beneficiario, ordenar_por, orden, pagina, cant_por_pagina
    )

    tipos_pago = listar_tipos_pagos()

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
@chequear_permiso("pago_crear")
@sesion_iniciada_requerida
def pago_crear():
    """Levanta el formulario para crear pagos y recibe los datos para enviarlos
    al modulo de pago y crear uno nuevo"""
    form = PagoForm()
    form.tipo_id.choices = [(tipo.id, tipo.nombre) for tipo in listar_tipos_pagos()]
    
    if request.method == "POST" and form.validate_on_submit():
        monto = form.monto.data
        descripcion = form.descripcion.data
        fecha_pago = form.fecha_pago.data
        tipo_id = form.tipo_id.data

        tipo_pago = obtener_tipo_pago(tipo_id)
        miembro_dni = form.dni.data if tipo_pago.nombre == 'Honorario' else None

        miembro_id = None
        if miembro_dni:
            miembro = obtener_miembro_dni(miembro_dni)
            if miembro:
                miembro_id = miembro.id
            else:
                flash(f"No se encontró ningún miembro con el DNI {miembro_dni}.", 'danger')
                return redirect(url_for('pago.pago_crear'))

        crear_pago(monto=monto, descripcion=descripcion, fecha_pago=fecha_pago, tipo_id=tipo_id, miembro_id=miembro_id)

        flash("Pago registrado con éxito.", 'success')
        return redirect(url_for('pago.pago_listar'))

    return render_template('pagos/crear.html', form=form, titulo="Crear pago")


@bp.route('/<int:id>', methods=['GET'])
@chequear_permiso("pago_mostrar")
@sesion_iniciada_requerida
def pago_mostrar(id):
    """Muestra la informacion del pago"""
    pago = obtener_pago(id)
    if pago.miembro_id:
        miembro = obtener_miembro(pago.miembro_id)
        beneficiario= miembro.dni
    else:
        beneficiario = ''
    return render_template('pagos/mostrar.html', pago=pago, beneficiario=beneficiario)

@bp.route('/<int:id>/eliminar', methods=['GET'])
@chequear_permiso("pago_eliminar")
@sesion_iniciada_requerida
def pago_eliminar(id):
    """Permite eliminar un pago del sistema, 
    toma el id y se lo envia la modulo de pago para hacer efectiva la baja"""
    eliminar_pago(id)
    flash("Pago eliminado con exito.", 'success')
    return redirect(url_for('pago.pago_listar'))

@bp.route("/<int:id>/editar/", methods=["GET", "POST"])
@chequear_permiso("pago_actualizar")
@sesion_iniciada_requerida
def pago_editar(id: int):
    """Controlador parar realizar la edicion del pago, 
    levanta el formulario con datos precargados"""
    pago = obtener_pago(id)
    form = PagoForm(obj=pago)
    if request.method == "GET" and (pago.miembro_id != None):
        form.dni.data = pago.miembro.dni
    form.tipo_id.choices = [(tipo.id, tipo.nombre) for tipo in listar_tipos_pagos()]

    if request.method == "POST" and form.validate_on_submit():
        pago.tipo_id = form.tipo_id.data
        pago.monto = form.monto.data
        pago.descripcion = form.descripcion.data
        pago.fecha_pago = form.fecha_pago.data        

        tipo_pago = obtener_tipo_pago(form.tipo_id.data)
        miembro_dni = form.dni.data if tipo_pago.nombre == 'Honorario' else None
        miembro_id = None
        if miembro_dni:
            miembro = obtener_miembro_dni(miembro_dni)
            if miembro:
                miembro_id = miembro.id
            else:
                flash(f"No se encontró ningún miembro con el DNI {miembro_dni}.", 'danger')
                return render_template("pagos/crear.html", form=form)
        pago.miembro_id = miembro_id    

        guardar_cambios()
        return redirect(url_for("pago.pago_listar"))

    return render_template("pagos/crear.html", form=form, titulo="Editar pago")
