from flask import render_template, request, redirect, url_for
from flask import Blueprint
from src.core.cobros import listar_cobros, crear_cobro, encontrar_cobro, guardar_cambios
from forms import CobroForm
from src.core.jinetes_y_amazonas.jinetes_y_amazonas import JineteOAmazona

bp = Blueprint("cobros", __name__, url_prefix="/cobros")

'''
    Retorna los cobros listados de manera ascendente según la fecha de pago
'''
@bp.get("/consultas")
def listar(asc: int = 1):
    try:
        ascendente = int(request.args.get('asc',1))
        pagina = int(request.args.get('pagina', 1))
        cant_por_pag = int(request.args.get('por_pag',2))
        cobros = listar_cobros(ascendente, pagina, cant_por_pag)
        ascendente = 0 if ascendente == 0 else 1
    except:
        cobros = listar_cobros()
    
    return render_template("cobros/listar.html", cobros_paginados=cobros, ascendente=ascendente)

@bp.route("/nuevo_cobro", methods=["GET", "POST"])
def nuevo_cobro():
    form = CobroForm()
    form.joa.choices = [(joa.id, joa.nombre +" "+ joa.apellido) for joa in JineteOAmazona.query.order_by('nombre')]
    if form.validate_on_submit():
        fecha_pago = form.fecha_pago.data
        medio_de_pago = form.medio_de_pago.data
        monto = form.monto.data
        observaciones = form.observaciones.data
        joa_id = form.joa.data
        crear_cobro(fecha_pago, medio_de_pago, monto, observaciones,joa_id)

        return redirect(url_for('cobros.listar'))

    return render_template("cobros/crear_cobro.html", form=form)


@bp.route("/editar_cobro/<string:id>", methods=["GET", "POST"])
def editar_cobro(id: str):
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

