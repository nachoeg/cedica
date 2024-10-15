from flask import Blueprint, render_template, request, redirect, url_for
from src.core.ecuestre import Ecuestre, TipoDeJyA, listar_ecuestres, listar_tipos_de_jya


bp = Blueprint("ecuestre", __name__, url_prefix="/ecuestre")


@bp.get("/")
def index():
    orden = request.args.get("orden", "asc")
    ordenar_por = request.args.get("ordenar_por", "id")
    pagina = int(request.args.get("pagina", 1))
    cant_por_pagina = int(request.args.get("cant_por_pagina", 10))
    nombre_filtro = request.args.get("nombre", "")
    tipo_jya_filtro = request.args.get("tipo_jya", "")

    query = Ecuestre.query.join(TipoDeJyA).filter(
        Ecuestre.nombre.ilike(f"%{nombre_filtro}%"),
        TipoDeJyA.tipo.ilike(f"%{tipo_jya_filtro}%"),
    )

    cant_resultados = query.count()

    if orden == "asc":
        query = query.order_by(getattr(Ecuestre, ordenar_por).asc())
    else:
        query = query.order_by(getattr(Ecuestre, ordenar_por).desc())

    ecuestres = query.paginate(page=pagina, per_page=cant_por_pagina, error_out=False)

    tipos_jya = listar_tipos_de_jya()

    cant_paginas = cant_resultados // cant_por_pagina
    if cant_resultados % cant_por_pagina != 0:
        cant_paginas += 1

    return render_template(
        "pages/ecuestre.html",
        ecuestres=ecuestres,
        tipos_jya=tipos_jya,
        cant_resultados=cant_resultados,
        cant_paginas=cant_paginas,
        pagina=pagina,
        orden=orden,
        ordenar_por=ordenar_por,
        tipo_jya_filtro=tipo_jya_filtro,
        nombre_filtro=nombre_filtro,
    )
