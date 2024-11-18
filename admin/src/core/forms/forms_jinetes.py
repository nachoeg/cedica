from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError
from wtforms.validators import (
    DataRequired, Length, Optional, Email)
from wtforms.fields import (
    DateField,
    SelectField,
    IntegerField,
    BooleanField,
    TextAreaField,
    SelectMultipleField,
    EmailField
)
import math
from core.forms.validaciones import Unico
from src.core.jinetes_y_amazonas.jinetes_y_amazonas import JineteOAmazona


def validar_telefono(form, campo):
    try:
        numero = campo.data
        num = int(numero)

        if math.log10(num)+1 < 7 or math.log10(num)+1 > 15:
            raise Exception()
    except ValueError:
        raise ValidationError('El número de teléfono sólo puede contener\
                               caracteres numéricos.')
    except Exception:
        raise ValidationError('El número de teléfono \
                              debe contener entre 7 y 15 digitos')


def validar_cadena_caracteres(form, campo):
    if any(caracter.isdigit() for caracter in campo.data):
        raise ValidationError('Este campo no puede contener números')


class NuevoJYAForm(FlaskForm):
    """
    Formulario utilizado para cargar
    la información general del jinete o amazona.
    """
    nombre = StringField('Nombre*', validators=[DataRequired('Ingrese \
                                    el nombre del jinete o la amazona'),
                                                validar_cadena_caracteres])
    apellido = StringField('Apellido*', validators=[DataRequired('Ingrese\
                                    el apellido del jinete o la amazona'),
                                                    validar_cadena_caracteres])
    dni = IntegerField('DNI*', validators=[
        Unico(JineteOAmazona, JineteOAmazona.dni),
        DataRequired('Ingrese el DNI del jinete o la amazona')])
    edad = IntegerField('Edad')
    fecha_nacimiento = DateField('Fecha de nacimiento*',
                                 validators=[
                                    DataRequired('Ingrese\
                                    la fecha de nacimiento\
                                    del jinete o la amazona')])
    provincia_nacimiento = StringField('Provincia de nacimiento',
                                       validators=[Length(max=64),
                                                   validar_cadena_caracteres])
    localidad_nacimiento = StringField('Localidad de nacimiento',
                                       validators=[Length(max=64),
                                                   validar_cadena_caracteres])
    domicilio_actual = StringField('Domicilio actual',
                                   validators=[Length(max=64)])
    telefono_actual = StringField('Telefono actual',
                                  validators=[Optional(), validar_telefono])
    contacto_emer_nombre = StringField('Nombre de contacto de emergencia',
                                       validators=[Length(max=64),
                                                   validar_cadena_caracteres])
    contacto_emer_telefono = StringField('Telefono de contacto de emergencia',
                                         validators=[Optional(),
                                                     validar_telefono])
    becado = BooleanField('¿Tiene beca?')
    porcentaje_beca = IntegerField('Porcentaje de beca', [Optional()])
    submit = SubmitField('Continuar')


class InfoSaludJYAForm(FlaskForm):
    """
    Formulario utilizado para
    cargar la información de salud del jinete o amazona.
    """

    certificado_discapacidad = BooleanField("¿Tiene certificado\
                                             de discapacidad?")
    diagnostico = SelectField("Diagnóstico", coerce=int)
    diagnostico_otro = StringField("Otro diagnóstico",
                                   validators=[Length(max=64)])
    tipo_discapacidad = SelectMultipleField(
        "Tipo de discapacidad", coerce=int)
    submit = SubmitField("Continuar")


class InfoEconomicaJYAForm(FlaskForm):
    """
    Formulario utilizado para cargar
    la información económica del jinete o amazona.
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
    num_afiliado = IntegerField("Numero de afiliado", validators=[Optional()])
    posee_curatela = BooleanField("¿Posee curatela?")
    observaciones_obra_social = StringField(
        "Observaciones", validators=[Length(max=64)]
    )
    submit = SubmitField("Continuar")


class InfoEscolaridadJYAForm(FlaskForm):
    """
    Formulario utilizado para cargar
    la información relacionada a la escolaridad del jinete o amazona.
    """

    nombre_escuela = StringField("Nombre de escuela",
                                 validators=[Length(max=40)])
    direccion_escuela = StringField("Direccion de escuela",
                                    validators=[Length(max=50)])
    telefono_escuela = StringField("Telefono de la escuela",
                                   validators=[Optional(), validar_telefono])
    grado_escuela = StringField("Grado al que asiste",
                                validators=[Length(max=4)])
    observaciones_escuela = StringField("Observaciones",
                                        validators=[Length(max=100)])
    profesionales_a_cargo = TextAreaField(
        "Profesionales a cargo*", validators=[
                                    Length(max=200),
                                    DataRequired('Ingrese al menos\
                                        un profesional a cargo\
                                        del jinete o la amazona'),
                                    validar_cadena_caracteres]
    )
    submit = SubmitField("Continuar")


class InfoInstitucionalJYAForm(FlaskForm):
    """
    Formulario utilizado para cargar
    la información institucional relacionada al jinete o amazona.
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
    profesor_id = SelectField("Profesor/Terapeuta", choices=[])
    conductor_caballo_id = SelectField("Conductor del caballo", choices=[])
    caballo_id = SelectField("Caballo asignado", choices=[])
    auxiliar_pista_id = SelectField("Auxiliar de pista", choices=[])
    dias = SelectMultipleField("Dias", coerce=int)
    submit = SubmitField("Finalizar carga")


class FamiliarForm(FlaskForm):
    parentesco = StringField("Parentesco", validators=[Length(max=40)])
    nombre = StringField("Nombre*", validators=[
        DataRequired("Debe ingresar un nombre"), Length(max=30)])
    apellido = StringField("Apellido*", validators=[
        DataRequired("Debe ingresar un apellido"), Length(max=30)])
    dni = IntegerField("DNI*", validators=[
        DataRequired("Debe ingresar un DNI")])
    domicilio_actual = StringField("Domicilio", validators=[Length(max=60)])
    telefono_actual = StringField('Telefono actual*',
                                  validators=[
                                    DataRequired("Debe ingresar un teléfono"),
                                    validar_telefono])
    email = EmailField(
        "Email",
        validators=[
            Optional(),
            Email("El mail debe contener '@' y '.'"),
        ])
    nivel_escolaridad = SelectField("Nivel de escolaridad",
                                    choices=[("pri", "Primario"),
                                             ("sec", "Secundario"),
                                             ("ter", "Terciario"),
                                             ("uni", "Universitario")])
    ocupacion = StringField("Ocupacion", validators=[Length(max=40)])
    submit = SubmitField("Aceptar")
