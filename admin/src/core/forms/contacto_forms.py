from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Optional, Length

class HistorialForm(FlaskForm):
    estado = SelectField('Estado', validators=[DataRequired('Debe seleccionar una opcion.')])
    comentario = StringField('Comentario', validators=[Optional(), Length(max=250, message="No puedo tener más de %(max)d caracteres.")])
    submit = SubmitField('Guardar')

