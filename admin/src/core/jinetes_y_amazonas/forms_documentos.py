from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms.fields import (
    FileField,
    SelectField,
    StringField,
    SubmitField,
)

class SubirArchivoForm(FlaskForm):
    titulo = StringField(
        "Titulo", validators=[DataRequired("Ingrese el nombre del documento")]
    )
    archivo = FileField("Archivo", validators=[DataRequired("Seleccione un archivo")])
    tipo_de_documento_id = SelectField("Tipo", choices=[('entrevista','Entrevista'),('evaluacion','Evaluación'),('planificacion','Planificación'),('evolucion','Evolución'),('documental','Documental')])
    submit = SubmitField("Guardar")


class EnlaceForm(FlaskForm):
    titulo = StringField(
        "Titulo", validators=[DataRequired("Ingrese el nombre del documento")]
    )
    url = StringField("Enlace", validators=[DataRequired("Ingrese el enlace")])
    tipo_de_documento_id = SelectField("Tipo", choices=[('entrevista','Entrevista'),('evaluacion','Evaluación'),('planificacion','Planificación'),('evolucion','Evolución'),('documental','Documental')])
    submit = SubmitField("Guardar")


class EditarArchivoForm(FlaskForm):
    titulo = StringField(
        "Titulo", validators=[DataRequired("Ingrese el nombre del documento")]
    )
    tipo_de_documento_id = SelectField("Tipo", coerce=int)
    submit = SubmitField("Guardar")

