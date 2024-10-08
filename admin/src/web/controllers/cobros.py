from flask import render_template, request, redirect, url_for
from flask import Blueprint
from src.core.cobros import listar_cobros, crear_cobro
from forms import CobroForm

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
    if form.validate_on_submit():
        fecha_pago = form.fecha_pago.data
        medio_de_pago = form.medio_de_pago.data
        monto = form.monto.data
        observaciones = form.observaciones.data
        crear_cobro(fecha_pago, medio_de_pago, monto, observaciones)

        return redirect(url_for('cobros.listar'))

    return render_template("cobros/crear_cobro.html", form=form)
