from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField, FileField
from wtforms.validators import DataRequired, Optional, NumberRange
from src.core.forms.validaciones import LimiteDeArchivo


class InfoMiembroForm(FlaskForm):
    nombre = StringField('Nombre*', validators=[DataRequired('Ingrese el nombre.')])
    apellido = StringField('Apellido*', validators=[DataRequired('Ingrese el apellido.')])
    dni = IntegerField('DNI*', validators=[DataRequired('Ingrese el DNI.')])
    email = StringField('Email¨*', validators=[DataRequired('Ingrese el email.')])
    telefono = IntegerField('Teléfono*', validators=[DataRequired('Ingrese el telefono.')])
    nombre_contacto_emergencia = StringField('Nombre del contacto de Emergencia*', validators=[DataRequired('Ingrese el nombre del contacto de emergencia.')])
    telefono_contacto_emergencia = IntegerField('Teléfono del contacto de Emergencia*', validators=[DataRequired('Ingrese el telefono del contacto de emergencia.'), NumberRange(min=-2147483648, max=2147483647, message="El valor exede los permitidos")])
    obra_social = StringField('Obra Social', validators=[Optional()])
    numero_afiliado = IntegerField('Número de Afiliado*', validators=[DataRequired('Ingrese el numero de afiliado')])
    condicion_id = SelectField('Condición de Trabajo*', validators=[DataRequired('Ingrese la condicion de trabajo.')])
    profesion_id = SelectField('Profesión*', validators=[DataRequired('Ingrese la profesión.')])
    puesto_laboral_id = SelectField('Puesto Laboral*', validators=[DataRequired('Ingrese el puesto laboral.')])
    calle = StringField('Calle*', validators=[DataRequired('Ingrese la calle.')])
    numero = IntegerField('Número*', validators=[DataRequired('Ingrese el numero.')])
    piso = IntegerField('Piso', validators=[Optional(), NumberRange(min=0, max=10000, message="El valor exede los permitidos")])
    dpto = StringField('Departamento', validators=[Optional()])
    localidad = StringField('Localidad*', validators=[DataRequired('Ingrese la localidad.')])
    alias = StringField('Alias', validators=[Optional()])
    submit = SubmitField('Guardar')

class ArchivoMiembroForm(FlaskForm):
    nombre = StringField(
        "Nombre", validators=[DataRequired("Ingrese el nombre del documento")]
    )
    archivo = FileField("Archivo", validators=[DataRequired("Seleccione un archivo"), LimiteDeArchivo(tamanio_en_mb=100)])
    tipo_de_documento_id = SelectField("Tipo", coerce=int, validators=[DataRequired("Seleccione una opcion")])    
    submit = SubmitField("Guardar")

class EditarArchivoMiembroForm(FlaskForm):
    nombre = StringField(
        "Nombre", validators=[DataRequired("Ingrese el nombre del documento")]
    )
    tipo_de_documento_id = SelectField("Tipo", coerce=int, validators=[DataRequired("Seleccione una opcion.")])
    submit = SubmitField("Guardar")


class EnlaceMiembroForm(FlaskForm):
    nombre = StringField(
        "Nombre", validators=[DataRequired("Ingrese el nombre del documento")]
    )
    url = StringField("Enlace", validators=[DataRequired("Ingrese el enlace.")])
    tipo_de_documento_id = SelectField("Tipo", validators=[DataRequired("Seleccione un opcion.")], coerce=int)
    submit = SubmitField("Guardar")