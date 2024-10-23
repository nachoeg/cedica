from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms.fields import (
    BooleanField,
    SelectField,
    DateField,
    StringField,
    SubmitField,
    SelectMultipleField,
)
from datetime import datetime


class EcuestreForm(FlaskForm):
    nombre = StringField(
        "Nombre", validators=[DataRequired("Ingrese el nombre del ecuestre")]
    )
    fecha_nacimiento = DateField(
        "Fecha de nacimiento",
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
    es_compra = BooleanField("¿Es compra?")
    fecha_ingreso = DateField(
        "Fecha de ingreso",
        validators=[DataRequired("Ingrese una fecha de ingreso")],
        default=datetime.now(),
    )
    sede = StringField(
        "Sede", validators=[DataRequired("Ingrese la sede del ecuestre")]
    )
    tipo_de_jya_id = SelectField("Tipo de Jinete y Amazona", coerce=int)
    conductores = SelectMultipleField("Conductores", coerce=int)
    entrenadores = SelectMultipleField("Entrenadores", coerce=int)
    submit = SubmitField("Guardar")
