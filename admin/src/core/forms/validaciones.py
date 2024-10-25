from wtforms.validators import ValidationError
from datetime import date


def LimiteDeArchivo(tamanio_en_mb):
    max_bytes = tamanio_en_mb * 1024 * 1024

    def chequear_tamanio(form, field):
        if len(field.data.read()) > max_bytes:
            raise ValidationError(
                f"El tamaño del archivo debe ser menor a {tamanio_en_mb}MB"
            )
        field.data.seek(0)

    return chequear_tamanio


def FechaNoFutura():

    def chequear_fechas(form, field):
        if field.data and field.data > date.today():
            raise ValidationError("La fecha no puede ser posterior a hoy")

    return chequear_fechas
