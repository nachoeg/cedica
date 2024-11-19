from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    SelectField
)
from wtforms.validators import (
    DataRequired,
    Length)
from wtforms.widgets import TextArea


class NuevoAnuncioForm(FlaskForm):
    """
    Formulario para crear un anuncio.
    El estado inicial siempre es Borrador
    """
    titulo = StringField('Titulo*', validators=[
        DataRequired('Ingrese el título del anuncio'),
        Length(max=200,
               message="El contenido no puede superar los %(max)d caracteres.")])
    copete = StringField('Copete*', validators=[
        DataRequired('Ingrese el copete del anuncio'),
        Length(max=500,
               message="El contenido no puede superar los %(max)d caracteres.")])
    contenido = StringField('Contenido*', validators=[
        DataRequired('Ingrese el contenido del anuncio'),
        Length(max=3000,
               message="El contenido no puede superar los %(max)d caracteres.")],
        widget=TextArea())
    guardar = SubmitField('Guardar borrador')


class EditarAnuncioForm(FlaskForm):
    """
    Formulario para editar un anuncio.
    """
    titulo = StringField('Titulo*', validators=[
        DataRequired('Ingrese el título del anuncio'),
        Length(max=200,
               message="El contenido no puede superar los %(max)d caracteres.")])
    copete = StringField('Copete*', validators=[
        DataRequired('Ingrese el copete del anuncio'),
        Length(max=500,
               message="El contenido no puede superar los %(max)d caracteres.")])
    contenido = StringField('Contenido*', validators=[
        DataRequired('Ingrese el contenido del anuncio'),
        Length(max=3000,
               message="El contenido no puede superar los %(max)d caracteres.")
               ],
        widget=TextArea())
    estado = SelectField('Estado', choices=[('bo', 'Borrador'),
                                            ('pu', 'Publicado'),
                                            ('ar', 'Archivado')])
    guardar = SubmitField('Aceptar')
