from urllib.parse import urlparse
from datetime import datetime, date

def booleano_a_palabra(bool):
    """Devuelve 'No' si el valor pasado por parámetro es False,
    'Sí' si es verdadero.
    """
    return ['No', 'Sí'][bool]


def palabra_a_booleano(palabra):
    """Devuelve True si el valor pasado por parámetro es 'Sí',
    False si es 'No'.
    """
    dicc = {'Sí': True, 'No': False, '': ''}
    return dicc[palabra]


def fechahora_a_fecha(fechahora):
    """Devuelve la fecha del parámetro con formato
    '%d-%m-%Y'.
    """
    return fechahora.strftime('%d-%m-%Y')


def fechahora(fechahora):
    """Devuelve fecha y hora del parámetro con formato
    '%d-%m-%Y %H:%M'.
    """
    return fechahora.strftime('%d-%m-%Y %H:%M')


def validar_url(url: str) -> str:
    """
    Ajusta la URL para asegurarse de que tenga un esquema válido.
    """
    parsed_url = urlparse(url)
    if not parsed_url.scheme:
        # Agregar http:// por defecto si no tiene esquema
        url = "http://" + url
    return url

def convertir_a_entero(valor, valor_predeterminado=1):
    """
    Intenta convertir el valor a un entero. Si falla, devuelve el valor predeterminado.
    """
    try:
        return int(valor)
    except (ValueError, TypeError):
        return valor_predeterminado


def calcular_edad(fecha_nacimiento):
    """
    Calcula la edad de una persona dada su fecha de nacimiento.
    """
    hoy = date.today()
    
    edad = hoy.year - fecha_nacimiento.year 
    - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
    return edad


def mostrar_dato(dato):
    if dato is None:
        return "-sin datos-"
    return dato
