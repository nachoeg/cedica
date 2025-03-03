import requests
from datetime import datetime
from src.core.anuncios import listar_anuncios_api, encontrar_anuncio
from src.core.contacto import crear_consulta
from src.web.schemas.anuncios import anuncios_schema, anuncio_schema
from src.web.schemas.contacto import consulta_schema, create_consulta_schema
from flask import Blueprint, request, current_app, make_response, jsonify


bp = Blueprint("api", __name__, url_prefix="/api")


def validar_captcha(token):
    """Esta funcion recibe un token de captcha y permite evaluar si es valido,
    para hacerlo llama a la API de Google"""
    secret_key = current_app.config.get("CAPTCHA_SECRET_KEY")
    url = "https://www.google.com/recaptcha/api/siteverify"

    payload = {"secret": secret_key, "response": token}

    try:
        response = requests.post(url, data=payload)

        result = response.json()

        if result.get("success"):
            return True
        else:
            return False
    except:
        return False


@bp.get("/articles")
def listar_anuncios():
    """Devuelve en formato JSON la lista de de articulos de noticias de forma paginada,
    devuelve, permite aplicar filtros por autor y fecha de publicacion"""
    try:
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 6))
        author = request.args.get("author") or None
        published_from = request.args.get("published_from") or None
        published_to = request.args.get("published_to") or None

        anuncios, cant_resultados = listar_anuncios_api(
            autor_filtro=author,
            despues_de_filtro=published_from,
            antes_de_filtro=published_to,
            pagina=page,
            cant_por_pag=per_page,
        )

        data = anuncios_schema.dump(anuncios)

        cant_paginas = cant_resultados // per_page
        if cant_resultados % per_page != 0:
            cant_paginas += 1

        response_body = {
            "data": data,
            "page": page,
            "per_page": per_page,
            "total": cant_resultados,
            "cant_pages": cant_paginas,
        }

        return make_response(jsonify(response_body), 200)
    except ValueError:
        return make_response(
            jsonify(
                {
                    "error": "Parámetros inválidos o faltantes en la solicitud.",
                }
            ),
            400,
        )
    except Exception as e:
        return make_response(
            jsonify(
                {
                    "error": f"Se produjo un error inesperado: {str(e)}",
                }
            ),
            500,
        )


@bp.get("/article/")
def obtener_anuncio():
    """
    Recibe un id y devuelve el anuncio guardado en el sistema con ese id
    """
    try:
        id = int(request.args.get("id"))

        if not id:
            return make_response(
                jsonify(
                    {
                        "error": "No se encontro un anuncio con el id especificado.",
                    }
                ),
                400,
            )

        anuncio = encontrar_anuncio(id)

        if not anuncio:
            return make_response(
                jsonify(
                    {
                        "error": "No se encontro un anuncio con el id especificado.",
                    }
                ),
                400,
            )
        data = anuncio_schema.dump(anuncio)

        return jsonify(data), 200
    except ValueError:
        return make_response(
            jsonify(
                {
                    "error": "Parámetros inválidos o faltantes en la solicitud.",
                }
            ),
            400,
        )
    except Exception as e:
        return make_response(
            jsonify(
                {
                    "error": f"Se produjo un error inesperado: {str(e)}",
                }
            ),
            500,
        )


@bp.post("/message")
def guardar_mensaje():
    """Recibe valores y crea una consulta en el sistema, valida los argumentos y un token captcha"""
    try:
        attrs = request.get_json()

        captcha_token = attrs.pop("captchaToken", None)

        if not captcha_token or not validar_captcha(captcha_token):
            return jsonify({"captcha": "Captcha inválido."}), 400

        errors = create_consulta_schema.validate(attrs)
        if errors:
            formatted_errors = {field: msgs[0] for field, msgs in errors.items()}
            return jsonify(formatted_errors), 400

        kwars = create_consulta_schema.load(attrs)
        consulta = crear_consulta(**kwars)

        consulta.created_at = datetime.now()
        consulta.status = "created"

        data = consulta_schema.dump(consulta)
        return jsonify(data), 201
    except:
        return make_response(
            jsonify(
                {
                    "error": "Parámetros inválidos o faltantes en la solicitud.",
                }
            ),
            400,
        )
