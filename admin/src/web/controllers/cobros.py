from flask import render_template, request
from flask import Blueprint
from src.core.cobros import listar_cobros, crear_cobro

bp = Blueprint("cobros", __name__, url_prefix="/consultas")

'''
    Retorna los cobros listados de manera ascendente según la fecha de pago
'''
@bp.get("/")
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
