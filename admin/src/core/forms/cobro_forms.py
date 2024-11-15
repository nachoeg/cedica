from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, Length, ValidationError
from wtforms.fields import DateField, SelectField, DecimalField, StringField, SubmitField, BooleanField
from datetime import date, datetime

class CobroForm(FlaskForm):
    ''' 
        Formulario para manejar la entidad Cobro.
    '''
    fecha_pago = DateField('Fecha de pago*', validators=[DataRequired('Ingrese una fecha de cobro')], default=datetime.now)
    medio_de_pago = SelectField('Medio de pago*', choices=[('efectivo', 'Efectivo'), ('credito', 'Tarjeta de crédito'), ('debito', 'Tarjeta de débito'), ('otro', 'Otro medio de pago')],render_kw={"placeholder": "Select one option"})
    monto = DecimalField('Monto*', validators=[DataRequired('Ingrese el monto que se cobró')])
    observaciones = StringField('Observaciones', validators=[Length(max=64)])
    joa = SelectField(u'Jinete o Amazona*', coerce=int)
    recibio_el_dinero = SelectField(u'Recibio el dinero*', coerce=int)
    submit = SubmitField('Aceptar')

    def validate_fecha_pago(self, fecha_pago):
        if fecha_pago.data and fecha_pago.data > date.today():
            raise ValidationError('La fecha de cobro no puede ser posterior a hoy.')
