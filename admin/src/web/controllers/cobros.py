from flask import render_template, request, redirect, url_for, flash
from flask import Blueprint
from src.core.cobros import (
    listar_cobros,
    crear_cobro,
    encontrar_cobro,
    guardar_cambios,
    cargar_joa_choices,
    cargar_miembro_activo_choices,
    listar_medios_de_pago,
    eliminar_cobro
)
from core.forms.cobro_forms import CobroForm
from src.web.handlers.decoradores import (
    sesion_iniciada_requerida,
    chequear_permiso)

bp = Blueprint("cobros", __name__, url_prefix="/cobros")


@bp.get("/")
@chequear_permiso("cobro_listar")
@sesion_iniciada_requerida
def listar():
    """
    Controlador que muestra el listado de cobros a J&A del sistema.
    """
    orden = request.args.get("orden", "asc")
    ordenar_por = request.args.get("ordenar_por", "id")
    pagina = int(request.args.get("pagina", 1))
    cant_por_pag = int(request.args.get("por_pag", 6))
    nombre_filtro = request.args.get("nombre", "")
    apellido_filtro = request.args.get("apellido", "")
    medio_pago_filtro = request.args.get("medio_de_pago", "")
    despues_de_filtro = request.args.get("despues_de", "")
    antes_de_filtro = request.args.get("antes_de", "")

    cobros, cant_resultados = listar_cobros(
        nombre_filtro,
        apellido_filtro,
        medio_pago_filtro,
        despues_de_filtro,
        antes_de_filtro,
        ordenar_por,
        orden,
        pagina,
        cant_por_pag,
    )

    medios_de_pago = listar_medios_de_pago()

    cant_paginas = cant_resultados // cant_por_pag
    if cant_resultados % cant_por_pag != 0:
        cant_paginas += 1

    return render_template(
        "pages/cobros/listar.html",
        cobros=cobros,
        medios_de_pago=medios_de_pago,
        cant_resultados=cant_resultados,
        cant_paginas=cant_paginas,
        pagina=pagina,
        orden=orden,
        ordenar_por=ordenar_por,
        nombre_filtro=nombre_filtro,
        apellido_filtro=apellido_filtro,
        medio_pago_filtro=medio_pago_filtro,
        despues_de_filtro=despues_de_filtro,
        antes_de_filtro=antes_de_filtro
    )


@bp.route("/nuevo_cobro", methods=["GET", "POST"])
@chequear_permiso("cobro_crear")
@sesion_iniciada_requerida
def nuevo_cobro():
    """
    Controlador que muestra el formulario de alta de un cobro
    o lo retorna para que sea guardado.
    """
    form = CobroForm()
    form.joa.choices = cargar_joa_choices()
    form.recibio_el_dinero.choices = cargar_miembro_activo_choices()

    if form.validate_on_submit():
        fecha_pago = form.fecha_pago.data
        medio_de_pago = form.medio_de_pago.data
        monto = form.monto.data
        observaciones = form.observaciones.data
        joa_id = form.joa.data
        recibio_el_dinero_id = form.recibio_el_dinero.data
        tiene_deuda = form.tiene_deuda.data

        crear_cobro(
            fecha_pago,
            medio_de_pago,
            monto,
            observaciones,
            joa_id,
            recibio_el_dinero_id,
            tiene_deuda
        )

        flash("Cobro guardado con éxito", "exito")
        return redirect(url_for("cobros.listar"))

    return render_template(
        "pages/cobros/crear_cobro.html", form=form, titulo="Nuevo cobro"
    )


@bp.get("/<int:id>/")
@chequear_permiso("cobro_mostrar")
@sesion_iniciada_requerida
def ver(id: int):
    """
    Controlador que permite la visualización de la información de un cobro.
    """
    cobro = encontrar_cobro(id)
    return render_template("pages/cobros/ver_cobro.html", cobro=cobro)


@bp.route("/<int:id>/editar/", methods=["GET", "POST"])
@chequear_permiso("cobro_actualizar")
@sesion_iniciada_requerida
def editar_cobro(id: int):
    """
    Controlador que muestra un formulario para editar un cobro
    o guarda la información cargada en él.
    """
    cobro = encontrar_cobro(id)
    form = CobroForm(obj=cobro)
    form.joa.choices = cargar_joa_choices()
    form.recibio_el_dinero.choices = cargar_miembro_activo_choices()

    if request.method == "GET":
        form.joa.data = cobro.joa.id
        form.medio_de_pago.data = cobro.medio_de_pago.name
        form.recibio_el_dinero.data = cobro.recibio_el_dinero.id
        form.tiene_deuda.data = cobro.tiene_deuda

    if request.method == "POST" and form.validate_on_submit():
        cobro.fecha_pago = form.fecha_pago.data
        cobro.medio_de_pago = form.medio_de_pago.data
        cobro.monto = form.monto.data
        cobro.observaciones = form.observaciones.data
        cobro.joa_id = form.joa.data
        cobro.recibio_el_dinero_id = form.recibio_el_dinero.data
        cobro.tiene_deuda = form.tiene_deuda

        guardar_cambios()

        flash("Cambios en el cobro guardados con éxito", "exito")
        return redirect(url_for("cobros.listar"))
    return render_template(
        "pages/cobros/crear_cobro.html", form=form, titulo="Editar cobro"
    )


@bp.get("/<int:id>/eliminar/")
@chequear_permiso("cobro_eliminar")
@sesion_iniciada_requerida
def eliminar(id: int):
    """
    Controlador que permite la eliminación de un cobro.
    """
    eliminar_cobro(id)
    flash("Cobro eliminado con éxito", "exito")

    return redirect(url_for("cobros.listar"))
