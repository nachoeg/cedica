from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, Length
from wtforms.fields import DateTimeField, SelectField, DecimalField, StringField, SubmitField, BooleanField
from datetime import datetime

class CobroForm(FlaskForm):
    fecha_pago = DateTimeField('Fecha de pago', format='%d/%m/%Y', validators=[DataRequired('Ingrese una fecha de pago')], default=datetime.now())
    medio_de_pago = SelectField('Medio de pago', choices=[('efectivo', 'Efectivo'), ('credito', 'Tarjeta de crédito'), ('debito', 'Tarjeta de débito'), ('otro', 'Otro medio de pago')])
    monto = DecimalField('Monto', validators=[DataRequired('Ingrese el monto que se cobró')])
    observaciones = StringField('Observaciones', validators=[Length(max=64)])
    joa = SelectField(u'Jinete o Amazona', coerce=int)
    recibio_el_dinero = SelectField(u'Recibio el dinero', coerce = int)
    tiene_deuda = BooleanField(u'¿Tiene deuda?', default=False)
    submit = SubmitField('Aceptar')
