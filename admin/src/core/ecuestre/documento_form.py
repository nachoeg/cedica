from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms.fields import (
    SelectField,
    StringField,
    SubmitField,
)


class DocumentoForm(FlaskForm):
    nombre = StringField(
        "Nombre", validators=[DataRequired("Ingrese el nombre del documento")]
    )
    tipo = SelectField("Tipo", coerce=int)
    submit = SubmitField("Guardar")
