from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, Length
from wtforms.fields import DateTimeField, SelectField, StringField, SubmitField, IntegerField, BooleanField, TextAreaField, SelectMultipleField
from datetime import datetime

#información general de la persona
class NuevoJYAForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired('Ingrese el nombre del jinete o la amazona')])
    apellido = StringField('Apellido', validators=[DataRequired('Ingrese el apellido del jinete o la amazona')])
    dni = IntegerField('DNI')
    edad = IntegerField('Edad')
    fecha_nacimiento =  DateTimeField('Fecha de nacimiento', format='%d/%m/%Y')
    provincia_nacimiento = StringField('Provincia de nacimiento', validators=[Length(max=64)])
    localidad_nacimiento = StringField('Localidad de nacimiento', validators=[Length(max=64)])
    domicilio_actual = StringField('Domicilio actual', validators=[Length(max=64)])
    telefono_actual = IntegerField('Telefono actual')
    contacto_emer_nombre = StringField('Nombre de contacto de emergencia', validators=[Length(max=64)])
    contacto_emer_telefono = IntegerField('Telefono de contacto de emergencia')
    becado = BooleanField('¿Tiene beca?')
    porcentaje_beca = StringField('Porcentaje de beca', validators=[Length(max=64)])
    submit = SubmitField('Continuar')


#información de salud
class InfoSaludJYAForm(FlaskForm):
    certificado_discapacidad = BooleanField('¿Tiene certificado de discapacidad?')
    diagnostico_id = SelectField(u'Diagnóstico', coerce=int)
    diagnostico_otro = StringField('Otro diagnóstico', validators=[Length(max=64)])
    tipo_discapacidad = SelectField('Tipo de discapacidad', choices=[('mental', 'Mental') , ('motora','Motora'), ('sensorial','Sensorial'), ('visceral','Visceral')])
    submit = SubmitField('Continuar')


#informacion economica
class InfoEconomicaJYAForm(FlaskForm):
    asignacion_familiar = BooleanField('¿Recibe asignación familiar?')
    tipo_asignacion_familiar = SelectField('Tipo de asignación familiar', choices=[('auhijo','Asignación Universal por hijo'),('auhdisc','Asignación Universal por hijo con Discapacidad'),('aaescolar','Asignación por ayuda escolar anual')])
    beneficiario_pension = BooleanField('¿Es beneficiario de alguna pensión?')
    tipo_pension = SelectField('Tipo de pensión', choices=[('provincial', 'Provincial'), ('nacional', 'Nacional')])
    obra_social = StringField('Obra social', validators=[Length(max=64)])
    num_afiliado = IntegerField('Numero de afiliado')
    posee_curatela = BooleanField('¿Posee curatela?')
    observaciones_obra_social = StringField('Observaciones', validators=[Length(max=64)])
    submit = SubmitField('Continuar')


#informacion sobre escolaridad y profesionales a cargo
class InfoEscolaridadJYAForm(FlaskForm):
    nombre_escuela = StringField('Nombre de escuela', validators=[Length(max=40)])
    direccion_escuela = StringField('Direccion de escuela', validators=[Length(max=50)])
    telefono_escuela = IntegerField('Telefono de la escuela')
    grado_escuela = StringField('Grado al que asiste', validators=[Length(max=4)])
    observaciones_escuela = StringField('Observaciones', validators=[Length(max=100)])
    profesionales_a_cargo = TextAreaField('Profesionales a cargo',validators=[Length(max=200)])
    submit = SubmitField('Continuar')

#trabajo en nuestra institucion
class InfoInstitucionalJYAForm(FlaskForm):
    propuesta_trabajo = SelectField('Propuesta de trabajo', choices=[('hipoterapia','Hipoterapia'),('monta_terapeutica','Monta terapéutica'),('deporte_ecuestre', 'Deporte ecuestre adaptado'), ('actividades_recreativas', 'Actividades recreativas'), ('equitacion', 'Equitación')])
    condicion = SelectField('Condicion', choices=[('regular','Regular'), ('de_baja', 'De baja')])
    sede = SelectField('Sede', choices=[('CASJ', 'CASJ'),('HLP','HLP'), ('otro', 'Otro')])
    dias = SelectMultipleField('Dias', choices=[('lun', 'Lunes'),('mar', 'Martes'),('mie', 'Miercoles'), ('jue', 'Jueves'),('vie', 'Viernes'),('sab', 'Sabado'), ('dom', 'Domingo') ])
    submit = SubmitField('Finalizar carga')

