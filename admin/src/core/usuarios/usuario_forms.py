from flask_wtf import FlaskForm
from wtforms import (BooleanField, EmailField, PasswordField,
                     SelectMultipleField, StringField)
from wtforms.validators import Email, InputRequired, Length
from core.usuarios.usuario import Rol


class UsuarioForm(FlaskForm):
    email = EmailField("Email", validators=[InputRequired(), Email()])
    contraseña = PasswordField(
        "Contraseña", 
        validators=[InputRequired(), 
                    Length(min=4, message="La contraseña debe tener por lo \
                        menos %(min)d caracteres")
                    ]
        )
    alias = StringField("Alias")
    admin_sistema = BooleanField("¿Es admin general?", default=False)
    roles = SelectMultipleField("Roles")

    def __init__(self, *args, **kwargs):
        super(UsuarioForm, self).__init__(*args, **kwargs)
        self.roles.choices = [(rol.id, rol.nombre) for rol in Rol.query.all()]
