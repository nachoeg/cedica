from flask_wtf import FlaskForm
from wtforms import (BooleanField, EmailField, PasswordField,
                     SelectMultipleField, StringField)
from wtforms.validators import (Email, InputRequired, Length)

from core.forms.validaciones import (Unico, sin_espacios,
                                     valor_en_opciones)
from core.usuarios import get_roles
from core.usuarios.usuario import Usuario


class UsuarioSinContraseñaForm(FlaskForm):
    """Clase que hereda de FlaskForm y representa el formulario de
    un usuario sin el campo 'contraseña'.
    """
    email = EmailField("Email", validators=[
        InputRequired("Debe ingresar un email."),
        Length(max=100, message="No puedo tener más de %(max)d caracteres."),
        Email("El mail debe contener '@' y '.'"),
        Unico(Usuario, Usuario.email, ilike=True, message="El mail ingresado \
            ya existe."),
        ])
    alias = StringField("Alias", validators=[
        InputRequired("Debe ingresar un alias."),
        Length(max=100, message="No puedo tener más de %(max)d caracteres."),
        Unico(Usuario, Usuario.alias, ilike=True, message="El alias ingresado \
              ya existe."),
        sin_espacios,
        ])
    admin_sistema = BooleanField("¿Es admin general?", default=False)
    roles = SelectMultipleField("Roles", coerce=int)

    def __init__(self, *args, **kwargs):
        """Construye los atributos necesarios para la
        clase UsuarioSinContraseñaForm.
        """
        super(UsuarioSinContraseñaForm, self).__init__(*args, **kwargs)
        # carga las opciones al campo roles
        opciones = [(rol.id, rol.nombre) for rol in get_roles()]
        self.roles.choices = opciones
        # agrega validación de que el valor recibido está entre las opciones
        id_opciones = [opcion[0] for opcion in self.roles.choices]
        self.roles.validators = [valor_en_opciones(id_opciones)]


class UsuarioForm(UsuarioSinContraseñaForm):
    """Clase que hereda de UsuarioSinContraseñaForm y representa
    el formulario de un usuario.
    """
    contraseña = PasswordField(
        "Contraseña",
        validators=[InputRequired("Debe ingresar una contraseña."),
                    Length(min=4, max=100, message="La contraseña debe \
                           tener por lo menos %(min)d caracteres."),
                    sin_espacios,
                    ]
        )
