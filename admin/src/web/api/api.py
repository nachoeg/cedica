from flask import Blueprint, request
import requests
from src.core.anuncios import listar_anuncios_api
from src.core.contacto import crear_consulta
from flask import request, make_response, jsonify
from datetime import datetime
from src.web.schemas.anuncios import anuncios_schema
from src.web.schemas.contacto import consulta_schema, create_consulta_schema
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

bp = Blueprint("api", __name__, url_prefix="/api")

def validar_captcha(token):
    secret_key = '6Ldhj4YqAAAAAJJOnlmmdh2bzzdWbDA3PgAJtFcc' 
    url = 'https://www.google.com/recaptcha/api/siteverify'
        
    payload = {'secret': secret_key, 'response': token}
    
    try:
        response = requests.post(url, data=payload)
        
        result = response.json()
        
        if result.get('success'):
            return True
        else:
            print(f"Captcha no validado: {result.get('error-codes')}")
            return False
    except Exception as e:
        print(f"Error al hacer la solicitud al API de reCAPTCHA: {e}")
        return False
        

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
        logger.debug(f"Datos recibidos: {attrs}")
        
        captcha_token = attrs.pop('captchaToken', None)
        logger.debug(f"Captcha token extraído: {captcha_token}")
        logger.debug(f"Datos recibidos: {attrs}")

        if not captcha_token:
            logger.error("Captcha inválido o ausente")
            return jsonify({"captcha": "Captcha inválido o ausente."}), 400

        if not validar_captcha(captcha_token):
            logger.error("Captcha no validado correctamente")
            return jsonify({"captcha": "Captcha inválido."}), 400

        errors = create_consulta_schema.validate(attrs)
        if errors:
            logger.warning(f"Errores de validación en los datos: {errors}")
            return jsonify(errors), 400

        kwars = create_consulta_schema.load(attrs)
        consulta = crear_consulta(**kwars)

        consulta.created_at = datetime.now()  
        consulta.closed_at = datetime.now()
        consulta.status = "created"

        data = consulta_schema.dump(consulta)
        return jsonify(data), 201

    except Exception as e:
        return make_response(jsonify({
            "error": "Ocurrió un error inesperado.",
            "detail": str(e)
        }), 400)