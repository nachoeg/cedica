from wtforms.validators import ValidationError
from datetime import date
from src.core.database import db


def TipoDeArchivo(permitidos):
    """
    Función que devuelve un validador que chequea que el archivo sea de un tipo permitido.
    """

    def chequear_tipo(form, field):
        if field.data.filename.split(".")[-1].lower() not in permitidos:
            raise ValidationError(
                f"El archivo debe ser de tipo {', '.join(permitidos)}"
            )

    return chequear_tipo


def LimiteDeArchivo(tamanio_en_mb):
    """
    Función que devuelve un validador que chequea que el tamaño del archivo no supere el límite en MB.
    """

    max_bytes = tamanio_en_mb * 1024 * 1024

    def chequear_tamanio(form, field):
        if len(field.data.read()) > max_bytes:
            raise ValidationError(
                f"El tamaño del archivo debe ser menor a {tamanio_en_mb}MB"
            )
        field.data.seek(0)

    return chequear_tamanio


def FechaNoFutura():
    """
    Función que devuelve un validador que chequea que la fecha no sea posterior a hoy.
    """

    def chequear_fechas(form, field):
        if field.data and field.data > date.today():
            raise ValidationError("La fecha no puede ser posterior a hoy")

    return chequear_fechas


class Unico(object):
    """Validador que verifica que el valor del campo
    sea único si se modificó.
    """

    def __init__(self, model, field, message=None):
        self.model = model
        self.field = field
        if message is None:
            message = "Este valor ya existe"
        self.message = message

    def __call__(self, form, field):
        """Permite llamar a la clase como una función"""
        if field.object_data == field.data:
            return
        check = (
            db.session.execute(db.select(self.model).where(self.field == field.data))
            .scalars()
            .all()
        )
        if check:
            raise ValidationError(self.message)


def valor_en_opciones(opciones):
    """Función que valida que el valor de un campo de formulario
    esté entre las opciones que recibe por parámetro.
    """
    mensaje = "El valor selecionado no está entre las opciones válidas."

    def _valor_en_opciones(form, field):
        if not set(field.data).issubset(set(opciones)):
            raise ValidationError(mensaje)

    return _valor_en_opciones


# def validar_email(form, field):
#     validacion = re.match(
#         r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', field.data)
#     if not validacion:
#         raise ValidationError("El mail debe contener '@' y '.'")

def validar_digitos(form, field):
    """Valida que el campo no contenga números."""
    if any(char.isdigit() for char in field.data):
        raise ValidationError("Este campo no puede contener números.")