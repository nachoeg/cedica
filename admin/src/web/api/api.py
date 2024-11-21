from src.core.database import db
from flask import Blueprint
from src.core.anuncios import listar_anuncios_api
from src.core import contacto
from flask import request, make_response, jsonify
from src.web.schemas.anuncios import anuncios_schema

bp = Blueprint("api", __name__, url_prefix="/api")

@bp.get("/articles")
def listar():
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 6))
        author = request.args.get('author') or None
        published_from = request.args.get('published_from') or None
        published_to = request.args.get('published_to') or None

        anuncios, cant_resultados = listar_anuncios_api(
            autor_filtro=author,
            despues_de_filtro=published_from,
            antes_de_filtro=published_to,
            pagina=page,
            cant_por_pag=per_page,
        )

        data = anuncios_schema.dump(anuncios)

        response_body = {
            "data": data,
            "page": page,
            "per_page": per_page,
            "total": cant_resultados,
        }

        return make_response(jsonify(response_body), 200)
    except Exception as e:
        return make_response(jsonify({
            "error": "Parámetros inválidos o faltantes en la solicitud.",
            "details": str(e)  # Incluye detalles para depuración.
        }), 400)