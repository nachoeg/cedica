from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
from wtforms.fields import (
    DateField,
    SelectField,
    IntegerField,
    BooleanField,
    TextAreaField,
    SelectMultipleField,
)

from core.forms.validaciones import Unico
from src.core.jinetes_y_amazonas.jinetes_y_amazonas import JineteOAmazona


class NuevoJYAForm(FlaskForm):
    """
    Formulario utilizado para cargar la información general del jinete o amazona.
    """
    nombre = StringField('Nombre*', validators=[DataRequired('Ingrese el nombre del jinete o la amazona')])
    apellido = StringField('Apellido*', validators=[DataRequired('Ingrese el apellido del jinete o la amazona')])
    dni = IntegerField('DNI*', validators=[Unico(JineteOAmazona, JineteOAmazona.dni), DataRequired('Ingrese el DNI del jinete o la amazona')])
    edad = IntegerField('Edad')
    fecha_nacimiento =  DateField('Fecha de nacimiento')
    provincia_nacimiento = StringField('Provincia de nacimiento', validators=[Length(max=64)])
    localidad_nacimiento = StringField('Localidad de nacimiento', validators=[Length(max=64)])
    domicilio_actual = StringField('Domicilio actual', validators=[Length(max=64)])
    telefono_actual = IntegerField('Telefono actual')
    contacto_emer_nombre = StringField('Nombre de contacto de emergencia', validators=[Length(max=64)])
    contacto_emer_telefono = IntegerField('Telefono de contacto de emergencia')
    becado = BooleanField('¿Tiene beca?')
    porcentaje_beca = StringField('Porcentaje de beca', validators=[Length(max=64)])
    submit = SubmitField('Continuar')


class InfoSaludJYAForm(FlaskForm):
    """
    Formulario utilizado para cargar la información de salud del jinete o amazona.
    """

    certificado_discapacidad = BooleanField("¿Tiene certificado de discapacidad?")
    diagnostico = SelectField("Diagnóstico", coerce=int)
    diagnostico_otro = StringField("Otro diagnóstico", validators=[Length(max=64)])
    tipo_discapacidad = SelectField(
        "Tipo de discapacidad",
        choices=[
            ("mental", "Mental"),
            ("motora", "Motora"),
            ("sensorial", "Sensorial"),
            ("visceral", "Visceral"),
        ],
    )
    submit = SubmitField("Continuar")


class InfoEconomicaJYAForm(FlaskForm):
    """
    Formulario utilizado para cargar la información económica del jinete o amazona.
    """

    asignacion_familiar = BooleanField("¿Recibe asignación familiar?")
    tipo_asignacion_familiar = SelectField(
        "Tipo de asignación familiar",
        choices=[
            ("auhijo", "Asignación Universal por hijo"),
            ("auhdisc", "Asignación Universal por hijo con Discapacidad"),
            ("aaescolar", "Asignación por ayuda escolar anual"),
        ],
    )
    beneficiario_pension = BooleanField("¿Es beneficiario de alguna pensión?")
    tipo_pension = SelectField(
        "Tipo de pensión",
        choices=[("provincial", "Provincial"), ("nacional", "Nacional")],
    )
    obra_social = StringField("Obra social", validators=[Length(max=64)])
    num_afiliado = IntegerField("Numero de afiliado")
    posee_curatela = BooleanField("¿Posee curatela?")
    observaciones_obra_social = StringField(
        "Observaciones", validators=[Length(max=64)]
    )
    submit = SubmitField("Continuar")


class InfoEscolaridadJYAForm(FlaskForm):
    """
    Formulario utilizado para cargar la información relacionada a la escolaridad del jinete o amazona.
    """

    nombre_escuela = StringField("Nombre de escuela", validators=[Length(max=40)])
    direccion_escuela = StringField("Direccion de escuela", validators=[Length(max=50)])
    telefono_escuela = IntegerField("Telefono de la escuela")
    grado_escuela = StringField("Grado al que asiste", validators=[Length(max=4)])
    observaciones_escuela = StringField("Observaciones", validators=[Length(max=100)])
    profesionales_a_cargo = TextAreaField(
        "Profesionales a cargo*", validators=[Length(max=200), DataRequired('Ingrese al menos un profesional a cargo del jinete o la amazona')]
    )
    submit = SubmitField("Continuar")


class InfoInstitucionalJYAForm(FlaskForm):
    """
    Formulario utilizado para cargar la información institucional relacionada al jinete o amazona.
    """

    propuesta_trabajo = SelectField(
        "Propuesta de trabajo",
        choices=[
            ("hipoterapia", "Hipoterapia"),
            ("monta_terapeutica", "Monta terapéutica"),
            ("deporte_ecuestre", "Deporte ecuestre adaptado"),
            ("actividades_recreativas", "Actividades recreativas"),
            ("equitacion", "Equitación"),
        ],
    )
    condicion = SelectField(
        "Condicion", choices=[("regular", "Regular"), ("de_baja", "De baja")]
    )
    sede = SelectField(
        "Sede", choices=[("CASJ", "CASJ"), ("HLP", "HLP"), ("otro", "Otro")]
    )
    profesor_id = SelectField("Profesor", choices=[])
    conductor_caballo_id = SelectField("Conductor del caballo", choices=[])
    caballo_id = SelectField("Caballo asignado", choices=[])
    auxiliar_pista_id = SelectField("Auxiliar de pista", choices=[])
    dias = SelectMultipleField(
        "Dias",
        choices=[
            ("lun", "Lunes"),
            ("mar", "Martes"),
            ("mie", "Miercoles"),
            ("jue", "Jueves"),
            ("vie", "Viernes"),
            ("sab", "Sabado"),
            ("dom", "Domingo"),
        ],
    )
    submit = SubmitField("Finalizar carga")
