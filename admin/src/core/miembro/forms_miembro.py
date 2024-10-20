from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField, FileField
from wtforms.validators import DataRequired, Optional

class InfoMiembroForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired('Ingrese el nombre.')])
    apellido = StringField('Apellido', validators=[DataRequired('Ingrese el apellido.')])
    dni = IntegerField('DNI', validators=[DataRequired('Ingrese el DNI.')])
    email = StringField('Email', validators=[DataRequired('Ingrese el email.')])
    telefono = IntegerField('Teléfono', validators=[DataRequired('Ingrese el telefono.')])
    nombreContactoEmergencia = StringField('Nombre del contacto de Emergencia', validators=[DataRequired('Ingrese el nombre del contacto de emergencia.')])
    telefonoContactoEmergencia = IntegerField('Teléfono del contacto de Emergencia', validators=[DataRequired('Ingrese el telefono del contacto de emergencia.')])
    obraSocial = StringField('Obra Social', validators=[Optional()])
    numeroAfiliado = IntegerField('Número de Afiliado', validators=[DataRequired('Ingrese el numero de afiliado')])
    condicion_id = SelectField('Condición de Trabajo', validators=[DataRequired('Ingrese la condicion de trabajo.')])
    profesion_id = SelectField('Profesión', validators=[DataRequired('Ingrese la profesión.')])
    puesto_laboral_id = SelectField('Puesto Laboral', validators=[DataRequired('Ingrese el puesto laboral.')])
    calle = StringField('Calle', validators=[DataRequired('Ingrese la calle.')])
    numero = StringField('Número', validators=[DataRequired('Ingrese el numero.')])
    piso = StringField('Piso', validators=[Optional()])
    dpto = StringField('Departamento', validators=[Optional()])
    localidad = StringField('Localidad', validators=[DataRequired('Ingrese la localidad.')])
    alias = StringField('Alias', validators=[Optional()])
    submit = SubmitField('Guardar')

class ArchivoMiembroForm(FlaskForm):
    nombre = StringField(
        "Nombre", validators=[DataRequired("Ingrese el nombre del documento")]
    )
    archivo = FileField("Archivo", validators=[DataRequired("Seleccione un archivo")])
    tipo = SelectField("Tipo", validators=[DataRequired("Seleccione un opcion.")], coerce=int)
    submit = SubmitField("Guardar")


class EnlaceMiembroForm(FlaskForm):
    nombre = StringField(
        "Nombre", validators=[DataRequired("Ingrese el nombre del documento")]
    )
    url = StringField("Enlace", validators=[DataRequired("Ingrese el enlace.")])
    tipo = SelectField("Tipo", validators=[DataRequired("Seleccione un opcion.")], coerce=int)
    submit = SubmitField("Guardar")