from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Optional, Length


class HistorialForm(FlaskForm):
    """Formulario para modificar el estado de una consulta, con su respectivo comentario"""

    estado = SelectField(
        "Estado", validators=[DataRequired("Debe seleccionar una opcion.")]
    )
    comentario = StringField(
        "Comentario",
        validators=[
            Optional(),
            Length(max=250, message="No puedo tener más de %(max)d caracteres."),
        ],
    )
    submit = SubmitField("Guardar")
