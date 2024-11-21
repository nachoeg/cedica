from flask import Blueprint
from src.core.anuncios import listar_anuncios_api
from src.core.contacto import crear_consulta
from flask import request, make_response, jsonify
from src.web.schemas.anuncios import anuncios_schema
from src.web.schemas.contacto import consulta_schema, create_consulta_schema

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
    except:
        return make_response(jsonify({
            "error": "Parámetros inválidos o faltantes en la solicitud.",
        }), 400)
    
@bp.post("/message")
def guardar_mensaje():
    try:
        attrs = request.get_json()
        errors = create_consulta_schema.validate(attrs)

        if errors:
            return jsonify(errors), 400
        else:
            kwars = create_consulta_schema.load(attrs)
            consulta = crear_consulta(**kwars)
            data = consulta_schema.dump(consulta)
            return jsonify(data), 201
    except Exception as e:
        return make_response(jsonify({
            "error": "Ocurrió un error inesperado.",
            "detail": str(e)
        }), 400)