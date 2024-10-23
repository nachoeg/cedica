from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SelectField, DateField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Optional, NumberRange, ValidationError
from src.core.pago import obtener_tipo_pago
from datetime import date

class PagoForm(FlaskForm):
    tipo_id = SelectField('Tipo de Pago', validators=[DataRequired('Debe seleccionar una opcion.')])
    monto = DecimalField('Monto', validators=[DataRequired('Debe de ingresar un monto.'), NumberRange(min=0.01, message="El monto debe ser mayor a 0")])
    descripcion = StringField('Descripción', validators=[Optional()])
    fecha_pago = DateField('Fecha de Pago', validators=[DataRequired('Debe ingresar una fecha de pago.')])
    dni = StringField('DNI', validators=[])  
    submit = SubmitField('Guardar')

    def validate_dni(self, dni):       
        tipo_pago = obtener_tipo_pago(self.tipo_id.data) 
        if tipo_pago.nombre == 'Honorario':
            if (dni.data is None or dni.data == ''):
                raise ValidationError('El campo DNI es obligatorio para pagos de tipo Honorario.')
        elif tipo_pago.nombre != 'Honorario':
            dni.data = None

    def validate_fechaDePago(self, fechaDePago):
        if fechaDePago.data and fechaDePago.data > date.today():
            raise ValidationError('La fecha de pago no puede ser posterior a hoy.')
