from datetime import date
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    DecimalField,
    SelectField,
    DateField,
    IntegerField,
    SubmitField,
)
from wtforms.validators import (
    DataRequired,
    Optional,
    NumberRange,
    ValidationError,
    Length,
)
from src.core.pago import obtener_tipo_pago


class PagoForm(FlaskForm):
    """Formulario para crear un nuevo pago en el sistema"""

    tipo_id = SelectField(
        "Tipo de Pago*", validators=[DataRequired("Debe seleccionar una opcion.")]
    )
    monto = DecimalField(
        "Monto*",
        validators=[
            DataRequired("Debe de ingresar un monto."),
            NumberRange(
                min=0.01, max=2147483647, message="El monto debe ser mayor a 0"
            ),
        ],
    )
    descripcion = StringField(
        "Descripción",
        validators=[
            Optional(),
            Length(max=250, message="No puedo tener más de %(max)d caracteres."),
        ],
    )
    fecha_pago = DateField(
        "Fecha de Pago*", validators=[DataRequired("Debe ingresar una fecha de pago.")]
    )
    miembro = SelectField("Miembro", coerce=int, validators=[Optional()])
    submit = SubmitField("Guardar")

    def validate_fechaDePago(self, fecha_pago):
        if fecha_pago.data and fecha_pago.data > date.today():
            raise ValidationError("La fecha de pago no puede ser posterior a hoy.")
        

    def validate_miembro_id(self, miembro_id):
        tipo_pago = obtener_tipo_pago(self.tipo_id.data)
        if tipo_pago.nombre == "Honorario" and not miembro_id.data:
            raise ValidationError(
                "Debe seleccionar un miembro para pagos de tipo Honorario."
            )
