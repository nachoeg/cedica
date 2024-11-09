from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms.fields import (
    FileField,
    SelectField,
    StringField,
    SubmitField,
)
from src.core.forms.validaciones import LimiteDeArchivo


class SubirArchivoForm(FlaskForm):
    """
    Formulario para la subida de un archivo
    """

    nombre = StringField(
        "Nombre", validators=[DataRequired("Ingrese el nombre del documento")]
    )
    archivo = FileField(
        "Archivo",
        validators=[
            DataRequired("Selecciona un archivo"),
            LimiteDeArchivo(tamanio_en_mb=100),
        ],
    )
    tipo_de_documento_id = SelectField("Tipo", coerce=int)
    submit = SubmitField("Guardar")


class EditarArchivoForm(FlaskForm):
    """
    Formulario para la edición de un archivo
    """

    nombre = StringField(
        "Nombre", validators=[DataRequired("Ingrese el nombre del documento")]
    )
    tipo_de_documento_id = SelectField("Tipo", coerce=int)
    submit = SubmitField("Guardar")


class EnlaceForm(FlaskForm):
    """
    Formulario para la creación de un enlace
    """

    nombre = StringField(
        "Nombre", validators=[DataRequired("Ingrese el nombre del documento")]
    )
    url = StringField("Enlace", validators=[DataRequired("Ingrese el enlace")])
    tipo_de_documento_id = SelectField("Tipo", coerce=int)
    submit = SubmitField("Guardar")
