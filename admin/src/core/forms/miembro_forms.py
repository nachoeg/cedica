from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField, FileField
from wtforms.validators import DataRequired, Optional, NumberRange, Email, Length
from src.core.forms.validaciones import LimiteDeArchivo, Unico, TipoDeArchivo
from src.core.miembro.miembro import Miembro


class InfoMiembroForm(FlaskForm):
    nombre = StringField('Nombre*', validators=[DataRequired('Ingrese el nombre.'), Length(max=100, message="No puedo tener más de %(max)d caracteres.")])
    apellido = StringField('Apellido*', validators=[DataRequired('Ingrese el apellido.'), Length(max=100, message="No puedo tener más de %(max)d caracteres.")])
    dni = IntegerField('DNI*', validators=[DataRequired('Ingrese el DNI.'), Unico(Miembro, Miembro.dni, message="El dni ya existe.")])
    email = StringField('Email¨*', validators=[DataRequired('Ingrese el email.'), Length(max=100, message="No puedo tener más de %(max)d caracteres."),
        Email("El mail debe contener '@' y '.'")
    ])
    telefono = IntegerField('Teléfono*', validators=[DataRequired('Ingrese el telefono.')])
    nombre_contacto_emergencia = StringField('Nombre del contacto de Emergencia*', validators=[DataRequired('Ingrese el nombre del contacto de emergencia.'), Length(max=100, message="No puedo tener más de %(max)d caracteres.")])
    telefono_contacto_emergencia = IntegerField('Teléfono del contacto de Emergencia*', validators=[DataRequired('Ingrese el telefono del contacto de emergencia.'), NumberRange(min=-2147483648, max=2147483647, message="El valor exede los permitidos")])
    obra_social = StringField('Obra Social', validators=[Optional(), Length(max=100, message="No puedo tener más de %(max)d caracteres.")])
    numero_afiliado = IntegerField('Número de Afiliado*', validators=[DataRequired('Ingrese el numero de afiliado'), NumberRange(min=0, max=10000000, message="El valor exede los permitidos")])
    condicion_id = SelectField('Condición de Trabajo*', validators=[DataRequired('Ingrese la condicion de trabajo.')])
    profesion_id = SelectField('Profesión*', validators=[DataRequired('Ingrese la profesión.')])
    puesto_laboral_id = SelectField('Puesto Laboral*', validators=[DataRequired('Ingrese el puesto laboral.')])
    calle = StringField('Calle*', validators=[DataRequired('Ingrese la calle.'), Length(max=100, message="No puedo tener más de %(max)d caracteres.")])
    numero = IntegerField('Número*', validators=[DataRequired('Ingrese el numero.'), NumberRange(min=0, max=10000000, message="El valor exede los permitidos")])
    piso = IntegerField('Piso', validators=[Optional(), NumberRange(min=0, max=10000, message="El valor exede los permitidos")])
    dpto = StringField('Departamento', validators=[Optional(), Length(max=100, message="No puedo tener más de %(max)d caracteres.")])
    localidad = StringField('Localidad*', validators=[DataRequired('Ingrese la localidad.'), Length(max=100, message="No puedo tener más de %(max)d caracteres.")])
    alias = StringField('Alias', validators=[Optional()])
    submit = SubmitField('Guardar')

class ArchivoMiembroForm(FlaskForm):
    nombre = StringField(
        "Nombre", validators=[DataRequired("Ingrese el nombre del documento"), Length(max=100, message="No puedo tener más de %(max)d caracteres.")]
    )
    archivo = FileField(
        "Archivo",
        validators=[
            DataRequired("Seleccione un archivo"),
            LimiteDeArchivo(tamanio_en_mb=100),
            TipoDeArchivo(permitidos=["pdf", "doc", "xls", "jpeg"]),
        ],
    )
    tipo_de_documento_id = SelectField("Tipo", coerce=int, validators=[DataRequired("Seleccione una opcion")])    
    submit = SubmitField("Guardar")

class EditarArchivoMiembroForm(FlaskForm):
    nombre = StringField(
        "Nombre", validators=[DataRequired("Ingrese el nombre del documento"), Length(max=100, message="No puedo tener más de %(max)d caracteres.")]
    )
    tipo_de_documento_id = SelectField("Tipo", coerce=int, validators=[DataRequired("Seleccione una opcion.")])
    submit = SubmitField("Guardar")


class EnlaceMiembroForm(FlaskForm):
    nombre = StringField(
        "Nombre", validators=[DataRequired("Ingrese el nombre del documento"), Length(max=100, message="No puedo tener más de %(max)d caracteres.")]
    )
    url = StringField("Enlace", validators=[DataRequired("Ingrese el enlace.")])
    tipo_de_documento_id = SelectField("Tipo", validators=[DataRequired("Seleccione un opcion.")], coerce=int)
    submit = SubmitField("Guardar")
