from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
from wtforms.fields import (
    FileField,
    SelectField,
    StringField,
    SubmitField,
)
from src.core.forms.validaciones import LimiteDeArchivo, TipoDeArchivo


class SubirArchivoForm(FlaskForm):
    """
    Formulario para la subida de un archivo
    """

    nombre = StringField(
        "Nombre",
        validators=[
            DataRequired("Ingrese el nombre del documento"),
            Length(max=100, message="No puede tener más de %(max)d caracteres."),
        ],
    )
    archivo = FileField(
        "Archivo",
        validators=[
            DataRequired("Selecciona un archivo"),
            LimiteDeArchivo(tamanio_en_mb=100),
            TipoDeArchivo(permitidos=["pdf", "doc", "xls", "jpeg"]),
        ],
    )
    tipo_de_documento_id = SelectField("Tipo", coerce=int)
    submit = SubmitField("Guardar")


class EditarArchivoForm(FlaskForm):
    """
    Formulario para la edición de un archivo
    """

    nombre = StringField(
        "Nombre",
        validators=[
            DataRequired("Ingrese el nombre del documento"),
            Length(max=100, message="No puede tener más de %(max)d caracteres."),
        ],
    )
    tipo_de_documento_id = SelectField("Tipo", coerce=int)
    submit = SubmitField("Guardar")


class EnlaceForm(FlaskForm):
    """
    Formulario para la creación de un enlace
    """

    nombre = StringField(
        "Nombre",
        validators=[
            DataRequired("Ingrese el nombre del documento"),
            Length(max=100, message="No puede tener más de %(max)d caracteres."),
        ],
    )
    url = StringField(
        "Enlace",
        validators=[
            DataRequired("Ingrese el enlace"),
            Length(max=100, message="No puede tener más de %(max)d caracteres."),
        ],
    )
    tipo_de_documento_id = SelectField("Tipo", coerce=int)
    submit = SubmitField("Guardar")
