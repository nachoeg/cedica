from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField
)
from wtforms.validators import (
    DataRequired,
    Length)


class AnuncioForm(FlaskForm):
    """
    Formulario para gestionar la entidad Anuncio
    """
    titulo = StringField('Titulo*', validators=[
        DataRequired('Ingrese el título del anuncio'), Length(max=200)])
    copete = StringField('Copete*', validators=[
        DataRequired('Ingrese el copete del anuncio'), Length(max=500)])
    contenido = StringField('Contenido*', validators=[
        DataRequired('Ingrese el contenido del anuncio'), Length(max=3000)])
    guardar_borrador = SubmitField('Guardar borrador')
    publicar = SubmitField('Publicar')
