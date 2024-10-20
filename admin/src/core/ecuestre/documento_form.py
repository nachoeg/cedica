from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms.fields import (
    FileField,
    SelectField,
    StringField,
    SubmitField,
)


class SubirArchivoForm(FlaskForm):
    nombre = StringField(
        "Nombre", validators=[DataRequired("Ingrese el nombre del documento")]
    )
    archivo = FileField("Archivo", validators=[DataRequired("Seleccione un archivo")])
    tipo = SelectField("Tipo", coerce=int)
    submit = SubmitField("Guardar")


class SubirEnlaceForm(FlaskForm):
    nombre = StringField(
        "Nombre", validators=[DataRequired("Ingrese el nombre del documento")]
    )
    url = StringField("Enlace", validators=[DataRequired("Ingrese el enlace")])
    tipo = SelectField("Tipo", coerce=int)
    submit = SubmitField("Guardar")
