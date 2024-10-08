from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, Length
from wtforms.fields import DateTimeField, SelectField, DecimalField, StringField, SubmitField
from datetime import datetime

from src.core.jinetes_y_amazonas.jinetes_y_amazonas import JineteOAmazona

class CobroForm(FlaskForm):
    fecha_pago = DateTimeField('Fecha de pago', format='%d/%m/%Y', validators=[DataRequired('Ingrese una fecha de pago')], default=datetime.now())
    medio_de_pago = SelectField('Medio de pago', choices=[('efectivo', 'Efectivo'), ('credito', 'Tarjeta de crédito'), ('debito', 'Tarjeta de débito'), ('otro', 'Otro medio de pago')])
    monto = DecimalField('Monto', validators=[DataRequired('Ingrese el monto que se cobró')])
    observaciones = StringField('Observaciones', validators=[Length(max=64)])
    joa = QuerySelectField(query_factory=lambda: JineteOAmazona.query.all())#ya no se hace asi
    submit = SubmitField('Aceptar')