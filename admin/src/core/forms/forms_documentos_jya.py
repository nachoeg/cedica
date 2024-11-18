import re
from src.core.forms.validaciones import LimiteDeArchivo, TipoDeArchivo
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired
from wtforms.fields import (
    FileField,
    SelectField,
)


def validar_sin_blancos(form, campo):
    """
    Función que evalúa si un campo de tipo string
    tiene espacios en blanco.
    """
    if re.search(r"\s", campo.data):
        raise ValidationError('El enlace no debe contener espacios.')


class SubirArchivoForm(FlaskForm):
    """
    Formulario utilizado para subir un archivo.
    """

    titulo = StringField(
        "Titulo", validators=[DataRequired("Ingrese el nombre del documento")]
    )
    archivo = FileField(
        "Archivo",
        validators=[
            DataRequired("Seleccione un archivo"),
            LimiteDeArchivo(tamanio_en_mb=2),
            TipoDeArchivo(permitidos=["pdf", "doc", "xls", "jpeg"]),
        ],
    )
    tipo_de_documento_id = SelectField(
        "Tipo",
        choices=[
            ("entrevista", "Entrevista"),
            ("evaluacion", "Evaluación"),
            ("planificacion", "Planificación"),
            ("evolucion", "Evolución"),
            ("documental", "Documental"),
        ],
    )
    submit = SubmitField("Guardar")


class EnlaceForm(FlaskForm):
    """
    Formulario utilizado para subir un enlace.
    """

    titulo = StringField(
        "Titulo", validators=[DataRequired("Ingrese el nombre del documento")]
    )
    url = StringField("Enlace", validators=[DataRequired("Ingrese el enlace"),
                                            validar_sin_blancos])
    tipo_de_documento_id = SelectField(
        "Tipo",
        choices=[
            ("entrevista", "Entrevista"),
            ("evaluacion", "Evaluación"),
            ("planificacion", "Planificación"),
            ("evolucion", "Evolución"),
            ("documental", "Documental"),
        ],
    )
    submit = SubmitField("Guardar")


class EditarArchivoForm(FlaskForm):
    """
    Formulario utilizado para editar un archivo.
    """

    titulo = StringField(
        "Titulo", validators=[DataRequired("Ingrese el nombre del documento")]
    )
    tipo_de_documento_id = SelectField("Tipo", coerce=int)
    submit = SubmitField("Guardar")
