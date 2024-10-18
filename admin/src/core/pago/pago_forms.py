from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SelectField, DateField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Optional, NumberRange, ValidationError
from datetime import date

class PagoForm(FlaskForm):
    tipo_id = SelectField('Tipo de Pago', choices=[
        ('provedor', 'Provedor'),
        ('honorario', 'Honorario'),
        ('gastos varios', 'Gastos varios')
    ], validators=[DataRequired()])
    
    monto = DecimalField('Monto', validators=[DataRequired(), NumberRange(min=0.01, message="El monto debe ser mayor a 0")])
    descripcion = StringField('Descripción', validators=[Optional()])
    fechaDePago = DateField('Fecha de Pago', validators=[DataRequired()])
    dni = IntegerField('DNI')  
    submit = SubmitField('Guardar')

    def validate_dni(self, dni):
        if self.tipo_id.data == 'honorario' and not dni.data:
            raise ValidationError('El campo DNI es obligatorio para pagos de tipo Honorario.')

    def validate_fechaDePago(self, fechaDePago):
        if fechaDePago.data and fechaDePago.data > date.today():
            raise ValidationError('La fecha de pago no puede ser posterior a hoy.')
