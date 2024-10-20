from flask import render_template, request, redirect, url_for
from flask import Blueprint
from src.core.cobros import listar_cobros, crear_cobro, encontrar_cobro, guardar_cambios, marcar_deuda
from src.core.cobros.cobro_forms import CobroForm
from src.core.jinetes_y_amazonas.jinetes_y_amazonas import JineteOAmazona
from src.core.miembro.miembro import Miembro

bp = Blueprint("cobros", __name__, url_prefix="/cobros")

'''
    Retorna los cobros listados de manera ascendente según la fecha de pago
'''
@bp.get("/")
def listar():
    orden = request.args.get("orden", "asc")
    ordenar_por = request.args.get("ordenar_por", "id")
    pagina = int(request.args.get('pagina', 1))
    cant_por_pag = int(request.args.get('por_pag',10))
    nombre_filtro = request.args.get("nombre", "")

    cobros = listar_cobros()
    cant_resultados = len(cobros.items)
    cant_paginas = cant_resultados // cant_por_pag
    if cant_resultados % cant_por_pag != 0:
        cant_paginas += 1
    
        return render_template(
        "cobros/listar.html",
        cobros=cobros,
        cant_resultados=cant_resultados,
        cant_paginas=cant_paginas,
        pagina=pagina,
        orden=orden,
        ordenar_por=ordenar_por,
        nombre_filtro=nombre_filtro,
    )

@bp.route("/nuevo_cobro", methods=["GET", "POST"])
def nuevo_cobro():
    form = CobroForm()
    form.joa.choices = [(joa.id, joa.nombre +" "+ joa.apellido) for joa in JineteOAmazona.query.order_by('nombre')]
    form.recibio_el_dinero.choices = [(miembro.id, miembro.nombre + " " + miembro.apellido) for miembro in Miembro.query.order_by('nombre')]
    if form.validate_on_submit():
        fecha_pago = form.fecha_pago.data
        medio_de_pago = form.medio_de_pago.data
        monto = form.monto.data
        observaciones = form.observaciones.data
        joa_id = form.joa.data
        recibio_el_dinero_id = form.recibio_el_dinero.data
        if form.tiene_deuda:
            marcar_deuda(joa_id)
        crear_cobro(fecha_pago, medio_de_pago, monto, observaciones,joa_id, recibio_el_dinero_id)

        return redirect(url_for('cobros.listar'))

    return render_template("cobros/crear_cobro.html", form=form)

@bp.get("/<int:id>/")
def ver(id: int):
    cobro = encontrar_cobro(id)
    return render_template("cobros/ver_cobro.html", cobro=cobro)

@bp.route("/<int:id>/editar/", methods=["GET", "POST"])
def editar_cobro(id: int):
    cobro = encontrar_cobro(id)
    print(cobro)
    form = CobroForm(obj=cobro)
    form.joa.choices = [(joa.id, joa.nombre +" "+ joa.apellido) for joa in JineteOAmazona.query.order_by('nombre')]
    form.joa.data = cobro.joa.id
    form.medio_de_pago.data = cobro.medio_de_pago.name
    print("Antes de entrar")
    if request.method == "POST" and form.validate_on_submit():
        cobro.fecha_pago = form.fecha_pago.data
        cobro.medio_de_pago = form.medio_de_pago.data
        cobro.monto = form.monto.data
        cobro.observaciones = form.observaciones.data
        cobro.joa_id = form.joa.data
        guardar_cambios()

        return redirect(url_for('cobros.listar'))
    return render_template('cobros/crear_cobro.html', form=form)

