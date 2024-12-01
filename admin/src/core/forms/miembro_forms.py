from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField, FileField
from wtforms.validators import DataRequired, Optional, NumberRange, Email, Length
from src.core.forms.validaciones import LimiteDeArchivo, Unico, validar_digitos, TipoDeArchivo
from src.core.miembro.miembro import Miembro

class InfoMiembroForm(FlaskForm):
    """Formulario para crear un nuevo miembro de equipo"""
    nombre = StringField('Nombre*', validators=[
        DataRequired('Ingrese el nombre.'),
        Length(max=100, message="No puede tener más de %(max)d caracteres."),
        validar_digitos
    ])
    apellido = StringField('Apellido*', validators=[
        DataRequired('Ingrese el apellido.'),
        Length(max=100, message="No puede tener más de %(max)d caracteres."),
        validar_digitos
    ])
    dni = IntegerField('DNI*', validators=[
        DataRequired('Ingrese el DNI.'),
        Unico(Miembro, Miembro.dni, message="El dni ya existe."),
        NumberRange(min=1000000, max=99999999, message="El DNI debe estar entre 1000000 y 99999999.")
    ])
    email = StringField('Email*', validators=[
        DataRequired('Ingrese el email.'),
        Length(max=100, message="No puede tener más de %(max)d caracteres."),
        Email("El email debe contener '@' y '.'")
    ])
    telefono = IntegerField('Teléfono*', validators=[
        DataRequired('Ingrese el teléfono.'),
        NumberRange(min=10000000, max=9999999999, message="El teléfono debe tener entre 8 y 10 dígitos.")
    ])
    nombre_contacto_emergencia = StringField('Nombre del contacto de Emergencia*', validators=[
        DataRequired('Ingrese el nombre del contacto de emergencia.'),
        Length(max=100, message="No puede tener más de %(max)d caracteres."),
        validar_digitos
    ])
    telefono_contacto_emergencia = IntegerField('Teléfono del contacto de Emergencia*', validators=[
        DataRequired('Ingrese el teléfono del contacto de emergencia.'),
        NumberRange(min=10000000, max=9999999999, message="El teléfono debe tener entre 8 y 10 dígitos.")
    ])
    obra_social = StringField('Obra Social', validators=[
        Optional(),
        Length(max=100, message="No puede tener más de %(max)d caracteres."),
        validar_digitos
    ])
    numero_afiliado = IntegerField('Número de Afiliado*', validators=[
        DataRequired('Ingrese el número de afiliado'),
        NumberRange(min=0, max=10000000, message="El valor excede los permitidos.")
    ])
    condicion_id = SelectField('Condición de Trabajo*', validators=[DataRequired('Ingrese la condición de trabajo.')])
    profesion_id = SelectField('Profesión*', validators=[DataRequired('Ingrese la profesión.')])
    puesto_laboral_id = SelectField('Puesto Laboral*', validators=[DataRequired('Ingrese el puesto laboral.')])
    calle = StringField('Calle*', validators=[
        DataRequired('Ingrese la calle.'),
        Length(max=100, message="No puede tener más de %(max)d caracteres."),
    ])
    numero = IntegerField('Número*', validators=[
        DataRequired('Ingrese el número.'),
        NumberRange(min=0, max=10000, message="El valor del número debe estar entre 0 y 10000.")
    ])
    piso = IntegerField('Piso', validators=[
        Optional(),
        NumberRange(min=0, max=100, message="El valor del piso debe estar entre 0 y 100.")
    ])
    dpto = StringField('Departamento', validators=[
        Optional(),
        Length(max=100, message="No puede tener más de %(max)d caracteres."),
        validar_digitos
    ])
    localidad = StringField('Localidad*', validators=[
        DataRequired('Ingrese la localidad.'),
        Length(max=100, message="No puede tener más de %(max)d caracteres."),
        validar_digitos
    ])
    alias = StringField('Alias', validators=[Optional()])
    submit = SubmitField('Guardar')

class ArchivoMiembroForm(FlaskForm):
    """Formulario para cargar archivos a un miembro de equipo"""
    nombre = StringField(
        "Nombre", validators=[DataRequired("Ingrese el nombre del documento"), Length(max=100, message="No puedo tener más de %(max)d caracteres.")]
    )
    archivo = FileField(
        "Archivo",
        validators=[
            DataRequired("Seleccione un archivo"),
            LimiteDeArchivo(tamanio_en_mb=100),
            TipoDeArchivo(permitidos=["pdf", "doc", "xls", "jpeg", "jpg", "docx"]),
        ],
    )
    tipo_de_documento_id = SelectField("Tipo", coerce=int, validators=[DataRequired("Seleccione una opcion")])    
    submit = SubmitField("Guardar")

class EditarArchivoMiembroForm(FlaskForm):
    """Formulario para editar los documentos cargados"""
    nombre = StringField(
        "Nombre", validators=[DataRequired("Ingrese el nombre del documento"), Length(max=100, message="No puedo tener más de %(max)d caracteres.")]
    )
    tipo_de_documento_id = SelectField("Tipo", coerce=int, validators=[DataRequired("Seleccione una opcion.")])
    submit = SubmitField("Guardar")


class EnlaceMiembroForm(FlaskForm):
    """"Formulario para modificar enlaces cargados a un miembro del equipo"""
    nombre = StringField(
        "Nombre", validators=[DataRequired("Ingrese el nombre del documento"), Length(max=100, message="No puedo tener más de %(max)d caracteres.")]
    )
    url = StringField("Enlace", validators=[DataRequired("Ingrese el enlace.")])
    tipo_de_documento_id = SelectField("Tipo", validators=[DataRequired("Seleccione un opcion.")], coerce=int)
    submit = SubmitField("Guardar")
