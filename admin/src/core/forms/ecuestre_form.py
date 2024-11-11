from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, ValidationError
from wtforms.fields import (
    BooleanField,
    SelectField,
    DateField,
    StringField,
    SubmitField,
    SelectMultipleField,
)
from src.core.forms.validaciones import FechaNoFutura
from datetime import date


def posterior_a_fecha_de_nacimiento(form, field):
    """
    Valida que la fecha de ingreso sea posterior o igual a la fecha de nacimiento.
    """
    fecha_nacimiento = form.fecha_nacimiento.data
    fecha_ingreso = field.data

    if fecha_nacimiento > fecha_ingreso:
        raise ValidationError(
            "La fecha de ingreso debe ser posterior o igual a la fecha de nacimiento."
        )


class EcuestreForm(FlaskForm):
    """
    Formulario para la creación de un ecuestre
    """

    nombre = StringField(
        "Nombre", validators=[DataRequired("Ingrese el nombre del ecuestre")]
    )
    fecha_nacimiento = DateField(
        "Fecha de nacimiento",
        validators=[
            DataRequired("Ingrese una fecha de nacimiento"),
            FechaNoFutura(),
        ],
        default=date.today(),
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
        validators=[
            DataRequired("Ingrese una fecha de ingreso"),
            posterior_a_fecha_de_nacimiento,
        ],
        default=date.today(),
    )
    sede = SelectField(
        "Sede", choices=[("CASJ", "CASJ"), ("HLP", "HLP"), ("otro", "Otro")]
    )
    tipo_de_jya_id = SelectField("Tipo de Jinete y Amazona", coerce=int)
    conductores = SelectMultipleField("Conductores", coerce=int)
    entrenadores = SelectMultipleField("Entrenadores", coerce=int)
    submit = SubmitField("Guardar")
