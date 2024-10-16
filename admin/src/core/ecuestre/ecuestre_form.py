from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, Length
from wtforms.fields import (
    DateTimeField,
    SelectField,
    DecimalField,
    StringField,
    SubmitField,
)
from datetime import datetime


class EcuestreForm(FlaskForm):
    nombre = StringField(
        "Nombre", validators=[DataRequired("Ingrese el nombre del ecuestre")]
    )
    fecha_nacimiento = DateTimeField(
        "Fecha de nacimiento",
        format="%d/%m/%Y",
        validators=[DataRequired("Ingrese una fecha de nacimiento")],
        default=datetime.now(),
    )
    sexo = SelectField("Sexo", choices=[("M", "Macho"), ("H", "Hembra")])
    raza = StringField(
        "Raza", validators=[DataRequired("Ingrese la raza del ecuestre")]
    )
    pelaje = StringField(
        "Pelaje", validators=[DataRequired("Ingrese el pelaje del ecuestre")]
    )
    es_compra = SelectField("Es compra", choices=[("True", "Sí"), ("False", "No")])
    fecha_ingreso = DateTimeField(
        "Fecha de ingreso",
        format="%d/%m/%Y",
        validators=[DataRequired("Ingrese una fecha de ingreso")],
        default=datetime.now(),
    )
    sede = StringField(
        "Sede", validators=[DataRequired("Ingrese la sede del ecuestre")]
    )
    tipo_de_jya_id = SelectField("Tipo de Jinete y Amazona", coerce=int)
    submit = SubmitField("Guardar")
